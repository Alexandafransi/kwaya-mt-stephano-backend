from rest_framework import serializers
from . import models


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SiteSettings
        fields = "__all__"


class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AboutPage
        fields = "__all__"


class KinandaProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KinandaProject
        fields = "__all__"


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        fields = "__all__"


class CommitteeMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommitteeMember
        fields = "__all__"


class CommitteeSerializer(serializers.ModelSerializer):
    members = CommitteeMemberSerializer(many=True, read_only=True)

    class Meta:
        model = models.Committee
        fields = "__all__"


class ChoirMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoirMember
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = "__all__"


class SongCategorySerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = models.SongCategory
        fields = "__all__"


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsItem
        fields = "__all__"


class HomilySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Homily
        fields = "__all__"


class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopItem
        fields = "__all__"


class ConstitutionArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConstitutionArticle
        fields = "__all__"


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GalleryImage
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Album
        fields = "__all__"
