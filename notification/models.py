from django.db import models
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from account.models import Account, Follow


class Notification(models.Model):
    Notification_Types = (
        (1, 'Like'),
        (2, 'Follow'),
        (3, 'Comment')
    )
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=Notification_Types)
    text_preview = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)


@receiver(post_save, sender=Follow)
def user_follow(sender, instance, created, **kwargs):
    if created:
        followers = instance.followers
        following = instance.following
        notify = Notification(sender=followers, user=following, notification_type=2)
        notify.save()


@receiver(pre_delete, sender=Follow)
def user_unfollow(sender, instance, **kwargs):
    followers = instance.followers
    following = instance.following
    notify = Notification.objects.filter(sender=followers, user=following, notification_type=2)
    if notify.exists():
        notify.delete()



# @receiver(post_save, sender=Follow)
# def user_follow(sender, instance, created, **kwargs):
#     if created:
#         follow = instance
#         sender = follow.followers
#         following = follow.following
#         notify = Notification.objects.filter(sender=sender, user=following, notification_type=2)
#         notify.save()
#
#
# @receiver(pre_delete, sender=Follow)
# def user_unfollow(sender, instance, **kwargs):
#     follow = instance
#     sender = follow.followers
#     following = follow.following
#     notify = Notification.objects.filter(sender=sender, user=following, notification_type=2)
#     notify.delete()
