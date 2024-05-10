from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, CursorPagination

from courses.models import Channel, Playlist, Video, Tag
from courses.serializers import ChannelSerializer, PlaylistSerializer, VideoSerializer, TagSerializer
from opentelemetry import trace
from silk.profiling.profiler import silk_profile
from django.core.cache import cache


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    
    
class NoCountPageNumberPagination(PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data):
        return Response(
            {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            }
        )

class CustomCursorPagination(CursorPagination):
    page_size = 10    
    ordering = '-created'

class ChannelViewset(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    TRACER = trace.get_tracer_provider().get_tracer(__name__)
    
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
    
    
class PlaylistViewset(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    TRACER = trace.get_tracer_provider().get_tracer(__name__)
    
    def get_queryset(self):
        return Playlist.objects.all()
        # return Playlist.objects.select_related('channel').all()
        # return Playlist.objects.select_related('channel').prefetch_related('videos__tags').all()
    
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
    
    
class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # pagination_class = CustomPageNumberPagination
    TRACER = trace.get_tracer_provider().get_tracer(__name__)

    def get_queryset(self):
        return Video.objects.all()
        # return Video.objects.select_related('playlist').all()
        # return Video.objects.select_related('playlist', 'playlist__channel').all()
        # return Video.objects.select_related('playlist', 'playlist__channel').prefetch_related('tags').all()
    
    # def list(self, request, *args, **kwargs):
    #     page = request.query_params.get('page', 1)
    #     cache_key = f"videos_page_{page}"

    #     cached_data = cache.get(cache_key)
    #     if cached_data:
    #         return Response(cached_data)
        
    #     response = super().list(self, request, *args, **kwargs)
    #     cache.set(cache_key, response.data, 30)
        
    #     return response


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    TRACER = trace.get_tracer_provider().get_tracer(__name__)
    