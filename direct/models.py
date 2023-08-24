# from django.db import models
# from account.models import Account, Follow
# from post.models import Post
#
#
# class DirectMessage(models.Model):
#     sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='from_user')
#     receiver = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='to_user')
#     message = models.TextField()
#     file = models.FileField(upload_to='direct_media/', null=True, blank=True)
#     is_read = models.BooleanField(blank=False)
#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['created_date']
#         verbose_name = 'Direct Message'
#         verbose_name_plural = 'Direct Messages'
#
#     def __str__(self):
#         return f'{self.sender} - {self.receiver}'
#
