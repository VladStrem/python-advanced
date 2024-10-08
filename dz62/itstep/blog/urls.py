дано проєкт з деяким кодом
views.py
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post, Category, Tag
from django.db.models import Avg, Q
from . import forms
from .forms import PostForm, RatingForm


# Create your views here.
###Posts
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save()
            messages.success(request, f"Post {new_post.title} was created")
            return redirect('blog:post-detail', new_post.pk)
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'blog/post/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'blog/post/create_post.html', {'form': form})


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            update_post = form.save()
            messages.success(request, f"Post {update_post.title} was updated")
            return redirect('blog:post-detail', update_post.pk)
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'blog/post/edit_post.html', {'form': form})
    form = PostForm(instance=post)
    return render(request, 'blog/post/edit_post.html', {'form': form})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f'Post "{post.title}" was deleted.')
        return redirect('blog:post-list') # Перенаправлення на список постів
    return render(request, 'blog/post/detail.html', {'post': post})

###
### Form
def create_tag(request):
    form = forms.TagFormModel(request.POST or None)
    if form.is_valid():
        tag = form.save()
        messages.success(request, f"Tag {tag.slug} was created")
        return redirect('blog:tag-create')
    elif request.method == "POST":
        messages.error(request, 'Please correct the error below.')
        return render(request, 'blog/tag/create_tag.html', {'form': form})
    tags = Tag.objects.all()
    return render(request, 'blog/tag/create_tag.html', {'form': form, 'tags': tags})


def edit_tag(request, pk=None):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = forms.TagFormModel(data=request.POST, instance=tag)
        if form.is_valid():
            updated_tag = form.save()
            messages.success(request, 'Tag "{}" was updated.'.format(updated_tag.slug))
            return redirect("blog:tag-create")
        tags = []
        return render(request, 'blog/tag/create_tag.html', {'form': form, "tags": tags})

    form = forms.TagFormModel(instance=tag)  # from obj to form
    tags = Tag.objects.all()
    return render(request, 'blog/tag/create_tag.html', {'form': form, "tags": tags})


def delete_tag(request, pk=None):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    messages.success(request, f"Tag {tag.slug} was deleted")
    # delete() returns how many objects were deleted and how many
    # deletions were executed by object type: (1, {'blog.Tag': 1})
    return redirect("blog:tag-create")


###

def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.published.filter(tags=tag)
    return render(request, 'blog/post/posts_by_tag.html', {'tag': tag, 'posts': posts})


def post_cards(request):
    posts = Post.objects.all()
    return render(request, "index.html", {'posts': posts})


####
def posts_list(request):
    post_list = Post.published.all().select_related('category')
    categories = Category.objects.all()

    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'categories': categories})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    avg_rating = post.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    ratings = post.ratings.select_related('user')
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'avg_rating': avg_rating,
        'ratings': ratings,
        'star_range': range(1, 6)
    })


def filter_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.published.filter(category=category)
    return render(request, 'blog/post/list.html', {'posts': posts, 'category': category})


def published_posts_list(request):
    posts = Post.published.all().select_related('category')
    return render(request, template_name="blog/post/published_list.html", context={'posts': posts})


def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()
    else:
        posts = Post.published.all()

    categories = Category.objects.all()
    return render(request, 'blog/post/list.html', {'posts': posts, 'query': query, 'categories': categories})
forms.py
from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'category', 'tags', 'publish']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'form-control'}),
            # 'image': forms.ClearableFileInput(attrs={'multiple': False}),
            'publish': forms.DateTimeInput(attrs={'type': 'datetime-local'})}
        labels = {'title': 'Назва публікації', 'body': 'Текст публікації'}


class TagForm(forms.Form):
    name = forms.CharField(label="Title for tag",
                           help_text="Enter your tag",
                           max_length=10)
    slug = forms.SlugField(max_length=31,
                           help_text="Enter your slug")

    # def save(self, instance, **kwargs):
    #     instance.update(**kwargs)
    #     instance.save()
    #     return instance


class TagFormModel(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

    def clean_name(self):
        value = self.cleaned_data['name']
        return value.lower()

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if len(slug) < 3:
            raise forms.ValidationError("Довжина менша за 3 символи")
        return slug

    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data.get("name")) < 3:
            self.add_error(None, "The total number of chars must be 3 or greate.")
urls.py
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

    path('cards/', views.post_cards, name='post-list-cards'),
    path('tag<slug:tag_slug>/', views.posts_by_tag, name='posts-by-tag'),

    path('tag/create', views.create_tag, name='tag-create'),
    path('tag/<int:pk>/update', views.edit_tag, name='tag-edit'),
    path('tag/<int:pk>/delete', views.delete_tag, name='tag-delete'),
]
detail.html
{% extends "base.html" %}
{% block title %} {{ post.title }} {% endblock %}
{% block content %}
<h1>{{ post.title }}</h1>

<p>
    Tags:
    {% for tag in post.tags.all %}
    <a href="{% url 'blog:posts-by-tag' tag.slug %}">{{ tag.name }}</a>{% if not forloop.last %}, {% endif %}
    {% endfor %}
</p>

<p class="date">
    Published {{ post.publish }}
</p>
{{ post.body|linebreaks }}

<a href="{% url 'blog:post-edit' post.pk %}"><button type="submit">Edit Post</button></a>

{% if request.user.is_superuser %}
<form action="{% url 'blog:post-delete' post.pk %}" method="post" style="display:inline;">
    {% csrf_token %}
    <button type="submit" onclick="return confirm('Ви впевнені, що хочете видалити цей пост?');">Видалити пост</button>
</form>
{% endif %}

{% endblock %}
І ось ЗАВДАННЯ
Домашня робота №68. Форми 
Добавити функціональність виставлення рейтингу поста залогованим користувачем (вхід користувача відбувається за допомогою admin-частини)
 у Django-додатку, використовуючи форму з зірочками для оцінювання
