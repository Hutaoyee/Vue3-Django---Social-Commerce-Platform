from django.urls import path

from .views import get_artist_list, get_album_list, get_music_list, get_video_list, get_notice_list

urlpatterns = [

    path('artists/', get_artist_list, name='artist-list'),
    path('albums/', get_album_list, name='album-list'),
    path('music/', get_music_list, name='music-list'),
    path('videos/', get_video_list, name='video-list'),
    path('notices/', get_notice_list, name='notice-list'),
]