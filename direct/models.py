from django.db import models
from account.models import Account, Follower, Following
from post.models import Post


class DirectMessage(models.Model):
    sender = models.ForeignKey(Follower, on_delete=models.CASCADE, null=True)
    reciever = models.ForeignKey(Following, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    file = models.FileField(upload_to='media/', null=True, blank=True)
    is_read = models.BooleanField(blank=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)



