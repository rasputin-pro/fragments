from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "created",
        "author",
        "group",
    )
    list_display_links = ("title",)
    list_editable = ("group",)
    search_fields = ("text",)
    list_filter = ("created",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "text",
        "created",
        "author",
    )
    list_filter = (
        "created",
        "post",
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )
    list_filter = (
        "user",
        "author",
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
