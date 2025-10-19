from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Video(models.Model):
    LOCAL = 'Local'
    YOUTUBE = 'YouTube'
    SOURCE_CHOICES = [
        (LOCAL, 'Local'),
        (YOUTUBE, 'YouTube'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)  # Thumbnail is optional for local uploads
    video_id = models.CharField(max_length=255, blank=True, null=True)  # Allow blank values
    upload_date = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    video_file = models.FileField(upload_to='videos/')
    dubbed_video_file = models.FileField(upload_to='dubbed_videos/', null=True, blank=True)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default=LOCAL)

    def save(self, *args, **kwargs):
        if not self.video_id and self.source == self.YOUTUBE:
            raise ValueError("YouTube videos must have a video_id.")
        if self.source == self.LOCAL and not self.video_id:
            self.video_id = f"local_{self.id or ''}"  # Auto-generate for local videos
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.text[:30]}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
