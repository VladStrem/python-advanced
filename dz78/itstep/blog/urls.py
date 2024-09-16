from django.urls import path
from . import views

app_name = "blog"


urlpatterns = [
    path('', views.posts_list, name='post-list'),

    path('post/list', views.PostList.as_view(template_name='blog/post/published_list.html'), name='posts-list'),

    path('search/', views.PostSearchView.as_view(), name='search-posts'),

    path('redirect/', views.MyRedirectView.as_view(), name='my-redirect'),

    path('category/<int:category_id>/', views.filter_by_category, name='filter-by-category'),  # Додано новий маршрут
    path('post/<int:id>/', views.post_detail, name='post-detail'),

    # path('post/<slug:slug>/', views.PostView.as_view(), name='post-detail-slug'),

    path('published/', views.published_posts_list, name='published-post-list'),

    # path('post/create/v2/', views.PostFormCreate.as_view(), name='post-create-v2'),
    path('post/create/', views.create_post, name='post-create'),
    path('post/create/v2/', views.PostFormCreate.as_view(), name='post-create-v2'),

    path('post/<slug:slug>/', views.PostView.as_view(), name='post-detail-slug'),
    path('post/<int:pk>/update/', views.edit_post, name='post-edit'),
    path('post/<int:pk>/delete/', views.delete_post, name='post-delete'),

    path('cards/', views.post_cards, name='post-list-cards'),

    path('cards/view', views.PostTemplateView.as_view(), name='post-list-cards-view'),

    path('tag<slug:tag_slug>/', views.posts_by_tag, name='posts-by-tag'),

    path('tag/create', views.create_tag, name='tag-create'),
    path('tag/<int:pk>/update', views.edit_tag, name='tag-edit'),
    path('tag/<int:pk>/delete', views.delete_tag, name='tag-delete'),
    path('tag/create/view', views.TagFormView.as_view(), name='tag-create-view'),

    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

]
