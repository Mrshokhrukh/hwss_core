from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions

from settings_module.models import AppConfig, MenuItem, Video
from settings_module.serializers import AppConfigSerializer, MenuItemSerializer


class AppConfigListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class MenuItemsAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        if self.request.user.is_authenticated:
            user_groups = self.request.user.groups.values_list("name", flat=True)
            queryset = queryset.filter(roles__name__in=user_groups).distinct()
        return queryset


@csrf_exempt
def get_videos(request):
    videos = Video.objects.all()
    data = []
    for video in videos:
        video_data = {
            "title": video.title,
            "thumbnail": video.thumbnail.url,
            "topic": video.topic,
            "description": video.description,
            "video_link": video.video_link,
            "video_file": video.video_file.url if video.video_file else None,
        }
        data.append(video_data)
    return JsonResponse(data, safe=False)
