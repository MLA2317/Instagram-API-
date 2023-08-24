from django.db import models
from account.models import Account, Follow
from django.db.models.signals import post_save


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
        return f'post of {self.user_id.username}'


class PostOtherAccount(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='other_account_post')
    users_id = models.ManyToManyField(Account,)


# class SendPost(models.Model):
#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
#     send = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True, blank=True)


class Like(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_like')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} || {self.user_id} - {self.post_id}'


class Comment(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follow_comment')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    top_level_comment_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'comment of {self.user_id} - {self.post_id}'

    @property
    def get_related_comments(self):
        qs = Comment.objects.filter(top_level_comment_id=self.id).exclude(id=self.id)
        if qs:
            return qs
        return None


def comment_post_save(instance, sender, created, *args, **kwargs):
    if created:
        top_level_comment = instance
        while top_level_comment.parent_comment:
            top_level_comment = top_level_comment.parent_comment
        instance.top_level_comment_id = top_level_comment.id
        instance.save()


post_save.connect(comment_post_save, sender=Comment)


class CommentLike(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comment_like_follower')
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)


