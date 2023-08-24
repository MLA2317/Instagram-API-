from django.contrib import admin
from .models import Post, PostOtherAccount, Like, Comment, CommentLike


# admin.site.register(Post)
admin.site.register(PostOtherAccount)
admin.site.register(Like)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'image', 'location', 'archive', 'send', 'created_date', 'update_date')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'parent_comment', 'top_level_comment_id', 'created_date')
    search_fields = ('user_id__username', 'user_id__first_name', 'user_id__last_name', 'post_id__image', 'top_level_comment_id')
    date_hierarchy = 'created_date'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'comment_id')
    search_fields = ('user_id__username', 'comment_id__message')
