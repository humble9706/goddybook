from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post

@receiver(m2m_changed, sender=Post.likes.through)
def users_like_changed(sender, instance, **kwargs):
	instance.total_likes = instance.likes.count()
	instance.save()