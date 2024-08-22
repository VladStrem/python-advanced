from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Tag
from django.db.models import Avg, Q


# Create your views here.
def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.published.filter(tags=tag)
    return render(request, 'blog/post/posts_by_tag.html', {'tag': tag, 'posts': posts})


def post_cards(request):
    posts = Post.objects.all()
    return render(request, "index.html", {'posts': posts})


####

def posts_list(request):
    posts = Post.published.all().select_related('category')
    categories = Category.objects.all()
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

