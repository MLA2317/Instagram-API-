from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import resolve, reverse_lazy
from django.db import transaction
from django.views.generic import CreateView
from .forms import AccountRegisterForm
from ..models import Account, Follow, Location
from post.models import Post, Save
from django.conf import settings
from django.contrib.auth.views import LoginView
from notification.models import Notification

Profile = settings.AUTH_USER_MODEL


class Register(CreateView):
    form_class = AccountRegisterForm
    success_url = reverse_lazy('account:login')  # reverse_lazy - bu qatga otvorish kere register qigandan keyin
    template_name = 'register/register.html'


class Login(LoginView):
    template_name = 'register/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('account:profile', kwargs={'username': self.request.user.username})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('account:sign-in')
    return render(request, 'register/register.html')


def profile(request, username):
    # Directly retrieve the account based on the username provided.
    account = get_object_or_404(Account, username=username)
    print(account)

    profiles = account
    if not request.user.is_authenticated:
        return redirect('account:sign-in')

    view = request.GET.get('view', 'posts')  # default to 'posts'


    if view == 'saved':
        saves = Post.objects.filter(save__account_id=account).order_by("-created_date")
        posts = Post.objects.none()
        print('sas', saves)
    else:
        posts = Post.objects.filter(user_id=account.id).order_by('-created_date')
        saves = Post.objects.none()
        print('posts', posts)
    print('save', saves)

    posts_count = posts.count()

    print('postscount', posts_count)
    following_count = Follow.objects.filter(following=account).count()
    followers_count = Follow.objects.filter(followers=account).count()
    follow_status = Follow.objects.filter(following=request.user, followers=account,).exists()
    print('ss', follow_status)

    # paginationu
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    user = get_object_or_404(Account, username=username)
    followers = Account.objects.filter(account_following__followers=user)
    print('followers', followers)
    following = Account.objects.filter(followers__following=user)
    print('following', following)

    context = {
        'posts': posts,
        'saves': saves,
        'profile': profiles,
        'posts_count': posts_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_paginator': posts_paginator,
        'follow_status': follow_status,
        'followings': following,
        'followers': followers,
        'view': view,
    }
    return render(request, 'profile/profile.html', context)


def EditProfile(request):
    user = request.user
    profile = Account.objects.get(username=user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        #date_of_birth = request.POST.get('date_of_birth', None)
        bio = request.POST.get('bio')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar')
        phone_number = request.POST.get('phone_number')
        location_title = request.POST.get('location')
        # print(location_title)
        # location = Location.objects.get(title=location_title)
        profile.location = location_title
        user.first_name = first_name
        user.last_name = last_name
        #profile.date_of_birth = date_of_birth
        profile.bio = bio
        profile.gender = gender
        user.email = email
        profile.avatar = avatar
        profile.phone_number = phone_number
        user.save()
        profile.save()
        return redirect('account:profile', username=user.username)
    
    context = {
        'profile': profile,
    }
    return render(request, 'profile/edit.html', context)


# def follow(request, username, option):
#     user = request.user
#     following = get_object_or_404(Account, username=username)
#
#     try:
#         f, created = Follow.objects.get_or_create(follower=request.user, following=following)
#
#         if int(option) == 0:
#             f.delete()
#             Follow.objects.filter(following=following, followers=request.user).all().delete()
#         else:
#             posts = Post.objects.all().filter(user=following)[:25]
#             with transaction.atomic():
#                 for post in posts:
#                     stream = Stream(post=post, user=request.user, date=post.posted, following=following)
#                     stream.save()
#         return HttpResponseRedirect(reverse('profile', args=[username]))
#
#     except User.DoesNotExist:
#         return HttpResponseRedirect(reverse('profile', args=[username]))

def follow(request, username, option):
    user = request.user
    followers = get_object_or_404(Account, username=username)

    try:
        # Using 'followers' and 'following' fields to match your model structure
        f, created = Follow.objects.get_or_create(followers=followers, following=request.user)
        print('f', f)
        print('created', created)

        if int(option) == 0:
            f.delete()
            # Delete the 'Follow' type notifications when someone unfollows
            Notification.objects.filter(sender=request.user, user=followers, notification_type=2).delete()
        else:
            # If there's a successful follow action, a notification is created.
            # No need to loop over posts as there's no 'Stream' functionality anymore.
            notify = Notification(
                sender=request.user,
                user=followers,
                notification_type=2,
                date=timezone.now(),
                is_seen=False
            )
            notify.save()

        return HttpResponseRedirect(reverse('account:profile', args=[username]))

    except Account.DoesNotExist:
        return HttpResponseRedirect(reverse('account:profile', args=[username]))
