# core django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.hashers import check_password


# project
from .forms import UserRegistrationForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if not user:
                u = User.objects.create_user(username, email, password)
                # add to group
                # expense_manager = Group.objects.get(name='expense_manager')
                # expense_manager.user_set.add(u)

                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('expense_manager:dashboard')
            else:
                stored_password = check_password(password, user.password)
                if stored_password:
                    raise forms.ValidationError(
                        'You already registered an account. Please log in.'
                    )
                else:
                    raise forms.ValidationError(
                        'Username has been taken. Try another username.'
                    )
        raise forms.ValidationError(
            'Registration has failed. Please try again.'
        )
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
