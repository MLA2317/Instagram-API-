from django.contrib import admin
from .models import Post, PostOtherAccount, Like, Comment, CommentLike


admin.site.register(Post)
admin.site.register(PostOtherAccount)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentLike)