from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification


@receiver(post_save, sender='post.Like')
def user_liked_post(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            post=instance.post_id,
            sender=instance.user_id,
            user=instance.post_id.user_id,
            notification_type=1,  # 1 for 'Like'
            text_preview=f"{instance.user_id.username} liked your post."
        )


@receiver(post_save, sender='account.Follow')
def user_followed_user(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            sender=instance.user,
            user=instance.followed,
            notification_type=2,  # 2 for 'Follow'
            text_preview=f"{instance.user.username} started following you."
        )


@receiver(post_save, sender='post.Comment')
def user_commented_on_post(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            post=instance.post,
            sender=instance.user,
            user=instance.post.author,
            notification_type=3,  # 3 for 'Comment'
            text_preview=f"{instance.user.username} commented on your post: {instance.text[:50]}..."  # Preview of the comment
        )