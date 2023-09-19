from django.contrib import admin
from .models import Post, Like, Comment, Save


admin.site.register(Like)
admin.site.register(Save)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'image', 'created_date', 'update_date')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'parent_comment', 'top_level_comment_id', 'created_date')
    search_fields = ('user_id__username', 'user_id__first_name', 'user_id__last_name', 'post_id__image', 'top_level_comment_id')
    date_hierarchy = 'created_date'

#
# @admin.register(CommentLike)
# class CommentLikeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user_id', 'comment_id')
#     search_fields = ('user_id__username', 'comment_id__message')
