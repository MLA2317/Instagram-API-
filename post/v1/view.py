from django.shortcuts import render, redirect, reverse
from ..models import Post, PostOtherAccount, Like, Comment, CommentLike
from account.models import Account, Follow
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    # # if not request.user.is_authenticated():
    # #     redirect('login')
    # user = request.user
    # all_users = Account.objects.all()
    # follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
    # # posts = Post.objects.filter(user_id=user)
    # ctx = {
    #     'all_users': all_users,
    #     'follow_status': follow_status
    #}
    ctx = {

    }
    return render(request, 'index.html', ctx)





