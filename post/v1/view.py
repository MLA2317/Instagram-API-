from django.core.paginator import Paginator
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from ..models import Post, PostOtherAccount, Like, Comment, Save
from account.models import Account, Follow
from django.contrib.auth.decorators import login_required
from .forms import NewPostform, CommentForm
from django.views import generic


@login_required()
def index(request):
    user = request.user
    follow_status = Follow.objects.filter(following=user, followers=request.user).exists()
    following_users = [follow.followers for follow in Follow.objects.filter(following=user)]
    print('following', following_users)
    all_users = Account.objects.exclude(id__in=[users.id for users in following_users]).exclude(id=user.id).order_by('?')[:50] #exclude - bu osha username borlarini chiqarmidi
    posts = Post.objects.filter(user_id__in=following_users).order_by('-created_date')
    print('post', posts)


    #groups_id = [post.id for post in posts]

    ctx = {
        'all_users': all_users,
        'my_user': following_users,
        'follow_status': follow_status,
        'posts': posts
    }
    return render(request, 'profile/../../template/post/index.html', ctx)


@login_required()
def explore(request):
    posts = Post.objects.all().order_by('?')

    #paginator
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    ctx = {
        'posts': posts
    }
    return render(request, 'explore/explore..html', ctx)

# Like function
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    print('post', post)
    current_likes = post.likes
    print('currien', current_likes)
    liked = Like.objects.filter(user_id=user, post_id=post).count()

    if not liked:
        Like.objects.create(user_id=user, post_id=post)
        current_likes = current_likes + 1
    else:
        Like.objects.filter(user_id=user, post_id=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    return HttpResponseRedirect(reverse('post:detail', args=[post_id]))


@login_required()
def new_post(request):
    user = request.user
    profile = get_object_or_404(Account, username=user)

    if request.method == 'POST':
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            location = form.cleaned_data.get('location')
            image = form.cleaned_data.get('image')
            description = form.cleaned_data.get('description')
            p, created = Post.objects.get_or_create(location=location, image=image, description=description, user_id=user)
            p.save()
            return redirect('account:profile', request.user.username)
    else:
        form = NewPostform()
    ctx = {
        'form': form
    }
    return render(request, 'profile/../../template/post/newpost.html', ctx)


# 1 - usul comment not working
# def detail(request, post_id):
#     user = request.user
#     posts = Post.objects.all()
#     post = Post.objects.get(pk=post_id)
#     comments = Comment.objects.filter(post_id=post).order_by('-created_date')
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return redirect('account:sign-up')
#         form = CommentForm(request.POST)
#         print('form', form)
#         if form.is_valid():
#             com = form.save(commit=False)
#             com.user_id = user
#             com.post_id = post
#             print(com.user_id)
#             com.save()
#             return redirect('.')
#         else:
#             print(form.errors)
#     else:
#         form = CommentForm()
#
#     ctx = {
#         'post': post,
#         'posts': posts,
#         'user': user,
#         'comments': comments,
#         'form': form,
#
#     }
#     return render(request, 'post/detail.html', ctx)


# 2 - usul

class PostDetail(generic.View):
    template_name = 'post/detail.html'
    lookup_field = 'pk'
    queryset = Post.objects.all()

    def get_object(self, pk): # bu post detail uchun
        try:
           post = self.queryset.get(id=pk)
           print('post', post)
        except Post.DoesNotExist:
            raise Http404()
        return post

    def get_context_data(self, pk, *args, **kwargs): # bu html da context olish uchun
        ctx = {
            'post': self.get_object(pk)
        }
        return ctx

    def get(self, request, pk): # bu post id ni malumotlarni olish uchun comment bilan
        ctx = self.get_context_data(pk)
        comments = Comment.objects.filter(post_id=pk, parent_comment__isnull=True).order_by('-created_date')
        print('commentss', comments)
        ctx['comments'] = comments
        return render(request, self.template_name, ctx)

    def post(self, request, pk, *args, **kwargs): # bu post id comment jonatish
        ctx = self.get_context_data(pk)

        if not request.user.is_authenticated:
            return redirect('account:sign-in')

        comment_id = request.GET.get('comment_id', None)
        user_id = request.user.id
        message = request.POST.get('body')
        if message:
            com = Comment.objects.create(user_id_id=user_id, post_id_id=pk, message=message, parent_comment_id=comment_id)
            return redirect(reverse('post:detail', kwargs={'pk': pk}) + f"#comments_{com.id}")
        return render(request, self.template_name, ctx)



@login_required
def saves(request, post_id):
    try:
        post_id = int(post_id)
    except ValueError:
        raise Http404('Invalid Post ID')

    post_to_save = get_object_or_404(Post, id=post_id)
    user_account = request.user.id

    saved_post, created = Save.objects.get_or_create(account_id_id=user_account, posts=post_to_save)
    print('save_post', saved_post, created)

    if not created:  # If post was already saved, then remove it
        saved_post.delete()

    return redirect('post:detail', pk=post_id)
