from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    # path("login/", views.user_login, name="login"),
    path("login/", views.LoginUser.as_view(), name="login"),
    # path("logout/", views.user_logout, name="logout"),
    path("logout/", auth_views.LogoutView.as_view(template_name="account:logged_out.html"), name="logout"),
    path("profile/", views.dashboard, name="dashboard"),

    path("register/", views.UserRegisterView.as_view(), name="register"),

    path("profile/edit/", views.edit_profile, name="profile-edit"),
    # path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile-edit"),
]
