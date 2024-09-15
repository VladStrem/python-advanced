from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post, Category, Rating, Tag
from django.db.models import Avg, Q
from . import forms
from .forms import PostForm, RatingForm
from django.contrib.auth.decorators import login_required


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
        else:
            messages.error(request, 'Error! Please check the form for issues.')

    form = forms.TagFormModel(instance=tag)  # from obj to form
    tags = Tag.objects.all()
    return render(request, 'blog/tag/create_tag.html', {
        'form': form,
        "tags": tags,
        'edit_mode': True
        })


def delete_tag(request, pk=None):
    tag = get_object_or_404(Tag, pk=pk)
    
    if request.method == "POST":
        tag.delete()
        messages.success(request, f"Tag {tag.slug} was deleted successfully.")
        return redirect("blog:tag-create")  # Редірект на список тегів після видалення
    
    return render(request, 'blog/tag/confirm_delete_tag.html', {'tag': tag})


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


# def posts_list(request):
#     posts = Post.published.all().select_related('category')
#     categories = Category.objects.all()
#     return render(request, 'blog/post/list.html', {'posts': posts, 'categories': categories})

# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     avg_rating = post.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
#     ratings = post.ratings.select_related('user')
    
#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating = form.save(commit=False)
#             rating.post = post
#             rating.user = request.user
#             existing_rating = Rating.objects.filter(post=post, user=request.user).first()
#             if existing_rating:
#                 existing_rating.rating = rating.rating
#                 existing_rating.save()
#                 messages.success(request, 'Your rating was updated.')
#             else:
#                 rating.save()
#                 messages.success(request, 'Thank you for rating this post!')
#             return redirect('blog:post-detail', post_id=post.id)
#     else:
#         form = RatingForm()

#     return render(request, 'blog/post/detail.html', {
#         'post': post,
#         'avg_rating': avg_rating,
#         'ratings': ratings,
#         'star_range': range(1, 6),
#         'form': form,
#     })
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    avg_rating = post.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    ratings = post.ratings.select_related('user')
    return render(request, 'blog/post/fssfsf.html', {
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
