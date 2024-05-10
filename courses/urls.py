from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import ChannelViewset, PlaylistViewset, VideoViewset, TagViewset


router = DefaultRouter()
router.register(r'channels', ChannelViewset, basename='channels')
router.register(r'playlists', PlaylistViewset, basename='playlists')
router.register(r'videos', VideoViewset, basename='vidoes')
router.register(r'tags', TagViewset, basename='tags')

urlpatterns = [
    path('api/', include(router.urls))
]
