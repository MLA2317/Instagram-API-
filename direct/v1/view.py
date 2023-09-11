from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from ..models import DirectMessage
from account.models import Account

@login_required()
def direct_inbox(request):
    user_id = request.user
    if not user_id.is_authenticated:
        return redirect('login')
    messages = DirectMessage.get_message(user_id=request.user)
    active_direct = None
    directs = None
    profile = get_object_or_404(Account, username=user_id)

    if messages:
        message = messages[0]
        active_direct = message['user_id'].username
        directs = DirectMessage.objects.filter(user_id=request.user, receiver=message['user_id'])
        print('direccttt', directs)
        directs.update(is_read=True)

        for message in messages:
            if message['user_id'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
    }
    return render(request, 'direct/direct.html', context)


@login_required
def directs(request, username): # error for user in direct message
    user_id = request.user
    messages = DirectMessage.get_message(user_id=user_id)
    print('message', messages)
    active_direct = username
    directs = DirectMessage.objects.filter(user_id=user_id, receiver__username=username)
    print('direct', directs)
    directs.update(is_read=True)

    for message in messages:
        print('mmm', message)
        if message['user_id'].username == username:
            message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'direct/direct.html', context)


def senddirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    message = request.POST.get('message')
    file = request.FILES.get('image')

    if request.method == "POST":
        to_user = Account.objects.get(username=to_user_username)
        DirectMessage.sender_message(from_user, to_user, message, file)
        return redirect('direct:message')


def usersearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = Account.objects.filter(Q(username__icontains=query))

        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
            }

    return render(request, 'direct/search.html', context)


def newconversation(request, username):
    from_user = request.user
    message = ''
    file = ''
    try:
        to_user = Account.objects.get(username=username)
        print('to_user', to_user)
    except Exception as e:
        return redirect('direct:search-users')
    if from_user != to_user:
        DirectMessage.sender_message(from_user, to_user, message, file)
    return redirect('direct:message')


