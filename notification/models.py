from django.db import models
from account.models import Account


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

    def __str__(self):
        return self.post