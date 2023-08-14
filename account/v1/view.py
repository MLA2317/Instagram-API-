from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse
from .forms import AccountRegisterForm, EditProfileForm


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






