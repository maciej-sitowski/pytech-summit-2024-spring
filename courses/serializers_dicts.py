from rest_framework import serializers

from courses.models import Channel, Playlist, Video, Tag
from opentelemetry import trace

from pytube import Playlist as YTPlaylist


def get_youtube_playlist_data(url):
    return YTPlaylist(url)


TRACER = trace.get_tracer_provider().get_tracer(__name__)

class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20)
    class Meta:
        model = Tag
        fields = ['id', 'name']


class SimplePlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'title', 'url']


class SimpleChannelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    url = serializers.URLField()
    
    def create(self, validated_data):
        return Channel.objects.create(**validated_data)    


class ChannelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    url = serializers.URLField()
    playlists = SimplePlaylistSerializer(many=True, read_only=True)
    
    def create(self, validated_data):
        return Channel.objects.create(**validated_data)    


class VideoSerializer(serializers.ModelSerializer):
    playlist = SimplePlaylistSerializer()
    channel = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    class Meta:
        model = Video
        fields = ['id', 'title', 'url', 'length', 'playlist', 'channel', 'tags']
        read_only_fields = fields
        
    def get_channel(self, obj):
        serializer = SimpleChannelSerializer(obj.playlist.channel)
        return serializer.data
    

class PlaylistSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(many=False, required=False, read_only=True)
    videos = VideoSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id','title', 'url', 'created_at', 'channel', 'videos']

    def create(self, validated_data):
        playlist_url = validated_data.get('url')
        youtube_playlist_data = get_youtube_playlist_data(playlist_url)
        
        channel_name = youtube_playlist_data.owner
        channel_url = youtube_playlist_data.owner_url
        channel, _ = Channel.objects.get_or_create(name=channel_name, url=channel_url)
        
        playlist, _ = Playlist.objects.get_or_create(
            url=playlist_url,
            title=youtube_playlist_data.title,
            channel=channel
        )
        
        videos = youtube_playlist_data.videos
        for video in videos:
            Video.objects.get_or_create(
                url=video.watch_url,
                length=video.length,
                title=video.title,
                playlist=playlist
            )

        return playlist
    
    