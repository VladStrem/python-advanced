from django.urls import path
from . import views

app_name = "blog"


urlpatterns = [
    path('', views.posts_list, name='post-list'),
    path('<int:id>/', views.post_detail, name='post-detail'),

    path('cards/', views.post_cards, name='post-list-cards'),
    path('tag<slug:tag_slug>/', views.posts_by_tag, name='posts-by-tag')
]
