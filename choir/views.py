from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers


class SingletonAPIView(APIView):
    """GET/PUT a singleton row (site settings, about page, kinanda project)."""

    model = None
    serializer_class = None

    def get(self, request):
        obj = self.model.load()
        return Response(self.serializer_class(obj, context={"request": request}).data)

    def put(self, request):
        obj = self.model.load()
        serializer = self.serializer_class(obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SiteSettingsView(SingletonAPIView):
    model = models.SiteSettings
    serializer_class = serializers.SiteSettingsSerializer


class AboutPageView(SingletonAPIView):
    model = models.AboutPage
    serializer_class = serializers.AboutPageSerializer


class KinandaProjectView(SingletonAPIView):
    model = models.KinandaProject
    serializer_class = serializers.KinandaProjectSerializer


class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = models.CalendarEvent.objects.all()
    serializer_class = serializers.CalendarEventSerializer
    filterset_fields = ["year", "month_index"]


class CommitteeViewSet(viewsets.ModelViewSet):
    queryset = models.Committee.objects.prefetch_related("members").all()
    serializer_class = serializers.CommitteeSerializer
    lookup_field = "slug"


class CommitteeMemberViewSet(viewsets.ModelViewSet):
    queryset = models.CommitteeMember.objects.all()
    serializer_class = serializers.CommitteeMemberSerializer
    filterset_fields = ["committee"]


class ChoirMemberViewSet(viewsets.ModelViewSet):
    queryset = models.ChoirMember.objects.all()
    serializer_class = serializers.ChoirMemberSerializer
    filterset_fields = ["voice_part"]


class SongCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.SongCategory.objects.prefetch_related("songs").all()
    serializer_class = serializers.SongCategorySerializer
    lookup_field = "slug"


class SongViewSet(viewsets.ModelViewSet):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer
    filterset_fields = ["category"]


class NewsItemViewSet(viewsets.ModelViewSet):
    queryset = models.NewsItem.objects.all()
    serializer_class = serializers.NewsItemSerializer
    lookup_field = "slug"


class HomilyViewSet(viewsets.ModelViewSet):
    queryset = models.Homily.objects.all()
    serializer_class = serializers.HomilySerializer
    lookup_field = "slug"


class ShopItemViewSet(viewsets.ModelViewSet):
    queryset = models.ShopItem.objects.all()
    serializer_class = serializers.ShopItemSerializer


class ConstitutionArticleViewSet(viewsets.ModelViewSet):
    queryset = models.ConstitutionArticle.objects.all()
    serializer_class = serializers.ConstitutionArticleSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = models.Album.objects.prefetch_related("images").all()
    serializer_class = serializers.AlbumSerializer
    lookup_field = "slug"


class GalleryImageViewSet(viewsets.ModelViewSet):
    queryset = models.GalleryImage.objects.all()
    serializer_class = serializers.GalleryImageSerializer
    filterset_fields = ["album"]
