from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post, Category
from django.db.models import Avg, Q


# Create your views here.

####
def posts_list(request):
    post_list = Post.objects.all().select_related('category')
    categories = Category.objects.all()

    paginator = Paginator(post_list, 6)
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
    avg_rating = round(post.ratings.aggregate(Avg('rating'))['rating__avg'] or 0, 2)
    ratings = post.ratings.select_related('user')
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'avg_rating': avg_rating,
        'ratings': ratings,
        'star_range': range(1, 6)
    })


def filter_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/post/list.html', {'posts': posts, 'category': category})


def published_posts_list(request):
    posts = Post.published.all().select_related('category')
    return render(request, template_name="blog/post/published_list.html", context={'posts': posts})


def filter_posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, status=Post.Status.PUBLISHED)
    categories = Category.objects.all()
    return render(request, 'blog/post/list.html', {'posts': posts, 'category': category, 'categories': categories})


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
