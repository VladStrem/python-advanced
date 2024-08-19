from django.shortcuts import render
from django.utils import timezone


def index(request):
    context = {'current_time': timezone.now()}
    return render(request, 'resume/index.html', context)


def about(request):
    return render(request, 'resume/about.html', {'current_time': timezone.now()})


def portfolio(request):
    return render(request, 'resume/portfolio.html', {'current_time': timezone.now()})
