from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

from blog.models import Post, Category, Tag
from django.db.models import Avg, Q, Count
from . import forms
from .forms import PostForm, TagFormModel, CommentForm
from django.views.generic import View, TemplateView, ListView, DetailView, FormView, CreateView, RedirectView, \
    UpdateView, DeleteView
from django.http import HttpResponseForbidden


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category/list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category/detail.html'
    context_object_name = 'category'


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ['title']
    template_name = 'blog/category/category_form.html'
    success_url = reverse_lazy('blog:category-list')
    success_message = "Category '%(title)s' was created successfully."


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['title']
    template_name = 'blog/category/category_form.html'
    success_url = reverse_lazy('blog:category-list')
    success_message = "Category '%(title)s' was updated successfully."


class CategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = Category
    template_name = 'blog/category/category_confirm_delete.html'
    success_url = reverse_lazy('blog:category-list')
    success_message = "Category was deleted successfully."


class PostList(View):
    template_name = 'blog/post/list.html'

    def get(self, request):
        posts = Post.published.all()
        return render(
            request,
            self.template_name,
            {'posts': posts}
        )

    def post(self, request):
        pass


# Create your views here.
###Posts
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            print(request.user)
            new_post.save()
            form.save_m2m()
            messages.success(request, f"Post {new_post.title} was created")
            return redirect('blog:post-detail', new_post.pk)
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'blog/post/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'blog/post/create_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author.pk == request.user.pk:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                update_post = form.save()
                messages.success(request, f"Post {update_post.title} was updated")
                return redirect('blog:post-detail', update_post.pk)
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'blog/post/edit_post.html', {'form': form})
        form = PostForm(instance=post)
        return render(request, 'blog/post/edit_post.html', {'form': form})
    else:
        return HttpResponseForbidden()


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f'Post "{post.title}" was deleted.')
        return redirect('blog:post-list')  # Перенаправлення на список постів
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


class PostTemplateView(ListView):
    # template_name = 'blog/post/post_list.html'
    model = Post
    context_object_name = 'posts'
    ordering = ['-title']

    def get_queryset(self):
        return super().get_queryset().filter(category__title="Python")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Post List View"
        return context


####
def posts_list(request):
    post_list = Post.published.all().select_related('category')
    # post_list = Post.objects.select_related('category').values('title', 'body', 'id', 'status', 'category')
    categories = Category.objects.all()

    paginator = Paginator(post_list, 10)
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

def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.annotate(count_tags=Count('tags')).select_related('category', 'author').prefetch_related('tags'),
        id=id)
    avg_rating = post.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    ratings = post.ratings.select_related('user')

    comments =post.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, "Your comment was added successfully.")
            return redirect('blog:post-detail', id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'avg_rating': avg_rating,
        'ratings': ratings,
        'star_range': range(1, 6),
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })


# def post_detail(request, id):
#     post = get_object_or_404(Post.objects.annotate(count_tags=Count('tags')).select_related('category', 'author').prefetch_related('tags'), id=id)
#     avg_rating = post.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
#     ratings = post.ratings.select_related('user')
#     return render(request, 'blog/post/detail.html', {
#         'post': post,
#         'avg_rating': avg_rating,
#         'ratings': ratings,
#         'star_range': range(1, 6)
#     })


class PostView(DetailView):
    model = Post
    # context_object_name = "post_obj"
    template_name = "blog/post/detail.html"  # blog/post_detail.html
    slug_field = "slug"


def filter_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.published.filter(category=category)
    return render(request, 'blog/post/list.html', {'posts': posts, 'category': category})


def published_posts_list(request):
    posts = Post.published.all().select_related('category')
    return render(request, template_name="blog/post/published_list.html", context={'posts': posts})


# def filter_posts_by_category(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     posts = Post.objects.filter(category=category, status=Post.Status.PUBLISHED)
#     categories = Category.objects.all()
#     return render(request, 'blog/post/list.html', {'posts': posts, 'category': category, 'categories': categories})


# def search_posts(request):
#     query = request.GET.get('q')
#     if query:
#         posts = Post.published.filter(
#             Q(title__icontains=query) | Q(body__icontains=query)
#         ).distinct()
#     else:
#         posts = Post.published.all()
#
#     categories = Category.objects.all()
#     return render(request, 'blog/post/list.html', {'posts': posts, 'query': query, 'categories': categories})


class PostSearchView(TemplateView):
    template_name = 'blog/post/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['posts'] = Post.published.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).distinct()
        else:
            context['posts'] = Post.published.all()
        context['query'] = query
        context['categories'] = Category.objects.all()
        return context


class MyRedirectView(RedirectView):
    url = reverse_lazy('blog:post-list')


class TagFormView(FormView):
    form_class = TagFormModel
    success_url = reverse_lazy('blog:tag-create')
    template_name = 'blog/tag/create_tag.html'

    def form_valid(self, form):
        tag = form.save()
        # messages.success(request, f"Tag {tag.slug} was created")
        return redirect(self.success_url)


# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             new_post = form.save()
#             messages.success(request, f"Post {new_post.title} was created")
#             return redirect('blog:post-detail', new_post.pk)
#         else:
#             messages.error(request, 'Please correct the error below.')
#             return render(request, 'blog/post/create_post.html', {'form': form})
#     form = PostForm()
#     return render(request, 'blog/post/create_post.html', {'form': form})


class PostFormCreate(CreateView):
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy('blog:post-list')
    template_name = 'blog/post/create_post.html'

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'id': self.object.id})
