from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Artist, Album, Music, Video, Notice
from .serializers import ArtistSerializer, AlbumSerializer, MusicSerializer, VideoSerializer, NoticeSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def get_artist_list(request):
    
    artist_queryset = Artist.objects.all()
    
    serializer = ArtistSerializer(artist_queryset, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_album_list(request):
    
    album_queryset = Album.objects.filter(is_active=True)
    
    # 添加查询参数过滤
    artist_id = request.GET.get('artist')
    if artist_id:
        album_queryset = album_queryset.filter(artist_id=artist_id)
    
    serializer = AlbumSerializer(album_queryset, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_music_list(request):
    
    music_queryset = Music.objects.filter(is_active=True)
    
    # 添加查询参数过滤
    album_id = request.GET.get('album')
    if album_id:
        music_queryset = music_queryset.filter(album_id=album_id)
    
    serializer = MusicSerializer(music_queryset, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_list(request):
    
    video_queryset = Video.objects.filter(is_active=True)
    
    serializer = VideoSerializer(video_queryset, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_notice_list(request):
   
    notice_queryset = Notice.objects.filter(is_active=True)
    
    serializer = NoticeSerializer(notice_queryset, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)