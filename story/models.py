from django.db import models
from account.models import Account, Follow


class Story(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.FileField(upload_to='story/')
    caption = models.TextField(null=True, blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id.username} - {self.content}'


class StoryMarkFollower(models.Model):
    story_id = models.ForeignKey(Story, on_delete=models.CASCADE)
    mark = models.ManyToManyField(Follow, blank=True)


class Archive(models.Model):
    story = models.OneToOneField(Story, on_delete=models.CASCADE)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archive of {self.story.user_id.username}"

