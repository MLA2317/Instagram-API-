from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import resolve

from .forms import AccountRegisterForm, EditProfileForm
from ..models import Account, Follow


def register(request):
    if request == 'POST':
        form = AccountRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            print('username', username)
            messages.success(request, f'Your account was created!')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('index.html')

    # elif request.user.is_authenticated:
    #     return redirect('sign-up')
    else:
        form = AccountRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'register/register.html', context)


# def UserProfile(request, username):
#     Account.objects.get_or_create(user=request.user)
#     user = get_object_or_404(Account, username=username)
#     profile = Account.objects.get(user=user)
#     url_name = resolve(request.path).url_name
#     posts = Post.objects.filter(user=user).order_by('-posted')
#
#     if url_name == 'profile':
#         posts = Post.objects.filter(user=user).order_by('-posted')
#     else:
#         posts = profile.favourite.all()
#
#     # Profile Stats
#     posts_count = Post.objects.filter(user=user).count()
#     following_count = Follow.objects.filter(follower=user).count()
#     followers_count = Follow.objects.filter(following=user).count()
#     # count_comment = Comment.objects.filter(post=posts).count()
#     follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
#
#     # pagination
#     paginator = Paginator(posts, 8)
#     page_number = request.GET.get('page')
#     posts_paginator = paginator.get_page(page_number)
#
#     context = {
#         'posts': posts,
#         'profile': profile,
#         'posts_count': posts_count,
#         'following_count': following_count,
#         'followers_count': followers_count,
#         'posts_paginator': posts_paginator,
#         'follow_status': follow_status,
#         # 'count_comment':count_comment,
#     }
#     return render(request, 'profile.html', context)




