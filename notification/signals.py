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
            sender=instance.following,
            user=instance.followers,
            notification_type=2,  # 2 for 'Follow'
            text_preview=f"{instance.followers.username} started following you."
        )


@receiver(post_save, sender='post.Comment')
def user_commented_on_post(sender, instance, created, **kwargs):
    if created:
        user_to_notify = instance.post_id.user_id

        Notification.objects.create(
            post=instance.post_id,
            sender=instance.user_id,
            user=user_to_notify,
            notification_type=3,  # 3 for 'Comment'
            text_preview=f"{instance.user_id.username} commented on your post: {instance.message[:50]}..."  # Preview of the comment
        )
