from django.db import models
from account.models import Account
from post.models import Post


class Save(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_save')
    user_id = models.ManyToManyField(Account,)
