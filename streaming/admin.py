from django.contrib import admin
from .models import Video, Comment

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'upload_date', 'view_count')
    search_fields = ('title', 'description')
    list_filter = ('upload_date',)
    raw_id_fields = ('owner',)
    ordering = ('-upload_date',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)
    raw_id_fields = ('video', 'user')
    ordering = ('-created_at',)

admin.site.register(Video, VideoAdmin)
admin.site.register(Comment, CommentAdmin)
