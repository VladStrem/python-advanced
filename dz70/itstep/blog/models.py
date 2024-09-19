from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')

    title = models.CharField(verbose_name="Назва поста", max_length=255)
    body = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True)

    image = models.ImageField(upload_to="post/images", default="default.png", blank=True, null=True)

    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True,
                                 related_name="posts")

    tags = models.ManyToManyField("Tag", related_name="blog_posts")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f'[{self.pk}] - {self.title}'

    class Meta:
        ordering = ["publish"]
        verbose_name_plural = "Публікації"
        verbose_name = "Публікації"

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.pk])

    def save(self, *args, **kwargs):  # < here
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        print("save to db")

    # def save(self, *args, **kwargs):
    #     print("save to db")
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True, help_text='A label for name tag.')
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config.')

    def __str__(self):
        return f'Tag<{self.name}>'

    class Meta:
        verbose_name = 'tags for posts'

    # def save(self, *args, **kwargs):
    #     print("save to db")
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.post.title} with {self.rating} stars"


class CommentPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

