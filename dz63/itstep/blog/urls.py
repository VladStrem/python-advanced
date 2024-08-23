from django.urls import path
from . import views

app_name = "blog"


urlpatterns = [
    path('', views.posts_list, name='post-list'),
    path('search/', views.search_posts, name='search-posts'),
    path('category/<int:category_id>/', views.filter_by_category, name='filter-by-category'),  # Додано новий маршрут
    path('<int:id>/', views.post_detail, name='post-detail'),
    path('published/', views.published_posts_list, name='published-post-list')
]
