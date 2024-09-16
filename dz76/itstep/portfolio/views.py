from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def redirect_to_hello(request):
    url = reverse("p-hi")
    print(url)
    return HttpResponseRedirect(url)


def hello(request):
    context = {"name": "world"}
    return render(request, "portfolio/home.html", context)


def about_me(request):
    context = f"About: info"
    return HttpResponse(content=context)


def my_skill(request, id):
    context = f"skill: id={id}"
    return HttpResponse(content=context)
