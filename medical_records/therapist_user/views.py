from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

from .forms import RegisterUserForm, LoginUserForm

from .models import Therapist

# Create your views here.
def login_user(request, *args, **kwargs):
    
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        print(user)
        print(user.id)
        if user is not None:
            login(request, user)
            print(dir(request.session))
            request.session['user_id'] = user.id
            return redirect("home")
        else:
            messages.error(request, ("there was an error"))

    return render(request, 'therapist_user/login.html', {})
    
    """ context = {}

    user = request.user

    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = LoginUserForm(request.POST)

        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context["login_form"] = form
    return render(request, 'therapist_user/login.html', context) """
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You were log out"))
    return redirect('home')


def register_user(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    
    context = {}

    if request.POST:
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            #account = authenticate(email=email, password=raw_password)
            login(request, new_user)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            context['registration_form'] = form

    return render(request, 'therapist_user/register_user.html', context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))

    return redirect
