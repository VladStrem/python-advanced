from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm


from .forms import LoginForm
# Журналізація виходу користувача:
import logging

from .models import Profile

logger = logging.getLogger(__name__)


# Create your views here.


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('account:password-change-done')
    success_message = "Password changed successfully!"

    def form_valid(self, form):
        logger.info(f"User {self.request.user.username} successfully changed their password.")
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"User {self.request.user.username} failed to change their password.")
        messages.error(self.request, 'There was an error. Please try again.')
        return super().form_invalid(form)


@login_required
def dashboard(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    return render(request,
                  'account/dashboard.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account:dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


class LoginUser(LoginView):
    form_class = AuthenticationForm
    authentication_form = None
    template_name = "account/login.html"
    # edirect_authenticated_user = 'account:dashboard'
    extra_context = {"title": "Login USER"}

    # def get_success_url(self):
    #     return reverse_lazy('account:dashboard')


def user_logout(request):
    logout(request)
    return redirect("blog:post-list-cards")


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:login')
    success_message = "Registration successfully! You can now log in."

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'There was an error with your registration. Please check the form for errors.')
        return super().form_invalid(form)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect("account:login")
        messages.error(request, 'There was an error with your registration. Please check the form for errors.')
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST,
                                       files=request.FILES,
                                       instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Update successful {request.user}!')
            return redirect('account:dashboard')
        else:
            messages.error(request, 'Was an error with update!!!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'account/edit.html'
    success_url = reverse_lazy('account:dashboard')
    success_message = 'Profile updated successfully!'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserEditForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserEditForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        user_form = UserEditForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your profile.")