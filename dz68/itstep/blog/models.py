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

    # def star_rating(self):
    #     return '★' * self.rating + '☆' * (5 - self.rating)

# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Post(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.title
#
#
# class Rating(models.Model):
#     RATING_CHOICES = [
#         (1, '1 Star'),
#         (2, '2 Stars'),
#         (3, '3 Stars'),
#         (4, '4 Stars'),
#         (5, '5 Stars'),
#     ]
#
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
#     score = models.IntegerField(choices=RATING_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ('post', 'user')
#
#     def __str__(self):
#         return f"{self.user.username} rated {self.post.title} with {self.score} stars"
