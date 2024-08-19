from django.urls import path
from .views import index, about, portfolio


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('portfolio/', portfolio, name='portfolio')
]