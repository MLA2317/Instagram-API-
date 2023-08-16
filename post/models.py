from django.db import models
from account.models import Account, Follow


class Post(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_post')
    image = models.ImageField(upload_to='user/post/image/')
    location = models.CharField(max_length=221, null=True, blank=True)
    description = models.TextField()
    archive = models.BooleanField(default=False)
    send = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.username} - post'


class PostOtherAccount(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='other_account_post')
    users_id = models.ManyToManyField(Follow,)


class Like(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_like')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f'{self.user_id.follower_set.count()} - {self.user_id.following_set.count()}'


class Comment(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follow_comment')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id} - {self.post_id}'


class CommentLike(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comment_liek_follower')
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)


