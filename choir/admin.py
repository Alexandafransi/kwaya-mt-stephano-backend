from django.contrib import admin
from . import models


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("name_en", "phone", "email")

    def has_add_permission(self, request):
        return not models.SiteSettings.objects.exists()


@admin.register(models.AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not models.AboutPage.objects.exists()


@admin.register(models.KinandaProject)
class KinandaProjectAdmin(admin.ModelAdmin):
    list_display = ("title_en", "raised_amount", "goal_amount")

    def has_add_permission(self, request):
        return not models.KinandaProject.objects.exists()


@admin.register(models.CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ("year", "month_name_en", "date", "title_en")
    list_filter = ("year", "month_index")
    search_fields = ("title_sw", "title_en")
    ordering = ("year", "month_index", "date")


class CommitteeMemberInline(admin.TabularInline):
    model = models.CommitteeMember
    extra = 1


@admin.register(models.Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ("name_en", "slug", "order")
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [CommitteeMemberInline]


@admin.register(models.ChoirMember)
class ChoirMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "voice_part", "joined_year")
    list_filter = ("voice_part",)
    search_fields = ("name",)


class SongInline(admin.TabularInline):
    model = models.Song
    extra = 1


@admin.register(models.SongCategory)
class SongCategoryAdmin(admin.ModelAdmin):
    list_display = ("name_en", "slug", "order")
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [SongInline]


@admin.register(models.NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title_en", "date", "slug")
    prepopulated_fields = {"slug": ("title_en",)}
    list_filter = ("date",)
    search_fields = ("title_sw", "title_en")


@admin.register(models.Homily)
class HomilyAdmin(admin.ModelAdmin):
    list_display = ("title_en", "date", "reading_en", "slug")
    prepopulated_fields = {"slug": ("title_en",)}
    list_filter = ("date",)
    search_fields = ("title_sw", "title_en")


@admin.register(models.ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ("name_en", "price", "order")


@admin.register(models.ConstitutionArticle)
class ConstitutionArticleAdmin(admin.ModelAdmin):
    list_display = ("heading_en", "order")
    ordering = ("order",)


class GalleryImageInline(admin.TabularInline):
    model = models.GalleryImage
    extra = 1


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title_en", "slug", "order")
    prepopulated_fields = {"slug": ("title_en",)}
    inlines = [GalleryImageInline]


@admin.register(models.GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "album", "order")
    list_filter = ("album",)
