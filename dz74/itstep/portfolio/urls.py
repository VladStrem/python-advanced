from django.urls import path

from .views import hello, about_me, my_skill, redirect_to_hello

urlpatterns = [
    path('hi/', hello, name="p-hi"),
    path('about/', about_me, name="p-about"),
    path('skills/<int:id>/<name>', my_skill, name="p-skill"),
    path('re/', redirect_to_hello, name="p-re")
]
