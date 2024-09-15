from django.urls import path
from . import views

app_name = "blog"


urlpatterns = [
    path('', views.posts_list, name='post-list'),
    path('search/', views.search_posts, name='search-posts'),
    path('category/<int:category_id>/', views.filter_by_category, name='filter-by-category'),  # Додано новий маршрут
    path('<int:id>/', views.post_detail, name='post-detail'),
    path('published/', views.published_posts_list, name='published-post-list'),

    path('post/create/', views.create_post, name='post-create'),
    path('post/<int:pk>/update/', views.edit_post, name='post-edit'),
    path('post/<int:pk>/delete/', views.delete_post, name='post-delete'),
    path('post/<int:post_id>/rate/', views.post_detail, name='rate-post'),

    path('cards/', views.post_cards, name='post-list-cards'),
    path('tag<slug:tag_slug>/', views.posts_by_tag, name='posts-by-tag'),

    path('tag/create', views.create_tag, name='tag-create'),
    path('tag/<int:pk>/update', views.edit_tag, name='tag-edit'),
    path('tag/<int:pk>/delete', views.delete_tag, name='tag-delete'),
]
