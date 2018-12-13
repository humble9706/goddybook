from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='Images')
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    slug = models.SlugField(max_length=100)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)#for purposes of denormalisation.

    class Meta:
        ordering = ('-total_likes', 'date')

    def __str__(self):
        return self.title

    # Use this method to automatically set the slug of the image.
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.date.year, self.date.month, self.date.day, self.slug, self.id])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{} commented on {}'.format(self.writer, self.post)