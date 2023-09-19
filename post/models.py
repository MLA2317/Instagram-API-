from django.db import models
from django.urls import reverse
from account.models import Account, Follow
from django.db.models.signals import post_save
from notification.models import Notification
from PIL import Image
import uuid


class Post(models.Model):
    #ids = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_post')
    image = models.FileField(upload_to='user/post/image/')
    description = models.TextField()
    likes = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # def get_absolute_url(self):
    #     return reverse("post-details", args=[str(self.ids)])

    def __str__(self):
        return f'post of {self.user_id.username}'

    @property
    def likes_count(self):
        return Like.objects.filter(post_id=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post_id=self).count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 600 or img.width > 480:
            output_size = (600, 480)
            img.thumbnail(output_size)
            img.save(self.image.path)


# class SendPost(models.Model):
#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
#     send = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True, blank=True)


class Like(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_like')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} || {self.user_id} - {self.post_id}'

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user)
        notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_types=1)
        notify.delete()


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

#
# class CommentLike(models.Model):
#     user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comment_like_follower')
#     comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)


class Save(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='save_post')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)

