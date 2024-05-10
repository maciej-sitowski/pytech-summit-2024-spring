from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.name}"
    

class Channel(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.url}"
    

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='playlists')
    
    def __str__(self):
        return f"{self.channel} - {self.title}"


class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    length = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='videos')
    tags = models.ManyToManyField(Tag, related_name='videos')
    
    def __str__(self) -> str:
        return f"{self.title}"