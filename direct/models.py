from django.db import models
from django.db.models import Max

from account.models import Account, Follow
from post.models import Post


class DirectMessage(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_id')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='from_user')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='to_user')
    message = models.TextField(max_length=10000, null=True, blank=True)
    file = models.FileField(upload_to='direct_media/', null=True, blank=True)
    is_read = models.BooleanField(blank=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def sender_message(cls, from_user, to_user, message, file):
        # sender uchun habarni saqlash
        sender_message = cls(
            user_id=from_user,
            sender=from_user,
            receiver=to_user,
            message=message,
            file=file,
            is_read=True
        )
        sender_message.save()

        # receiver uchun habarni saqlash
        receiver_message = cls(
            user_id=to_user,
            sender=from_user,
            receiver=from_user,
            message=message,
            file=file,
            is_read=False # qabul qiluvchi habarni hali oqimagan
        )
        receiver_message.save()

    # @classmethod
    # def mark_is_read(cls, user_id, sender_id):
    #     # Qabul qiluvchiga yuborilgan, lekin hali o'qilmagan habarlarni o'qilgan deb belgilash
    #     unread_message = cls.objects.filter(user_id=user_id, sender=sender_id, is_read=False)
    #     unread_message.update(is_read=True)


    def get_message(user_id):
        users = []
        messages = DirectMessage.objects.filter(user_id=user_id).values('receiver').annotate(last=Max('created_date')).order_by('-last')
        print('messsss', messages)
        for message in messages:
            users.append({
                'user_id': Account.objects.get(pk=message['receiver']),
                'last': message['last'],
                'unread': DirectMessage.objects.filter(user_id=user_id, receiver__pk=message['receiver'], is_read=False).count()
            })
        return users

    class Meta:
        ordering = ['created_date']
        verbose_name = 'Direct Message'
        verbose_name_plural = 'Direct Messages'

    def __str__(self):
        return f'{self.sender} - {self.receiver}'


