from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("calendar-events", views.CalendarEventViewSet)
router.register("committees", views.CommitteeViewSet)
router.register("committee-members", views.CommitteeMemberViewSet)
router.register("members", views.ChoirMemberViewSet)
router.register("song-categories", views.SongCategoryViewSet)
router.register("songs", views.SongViewSet)
router.register("news", views.NewsItemViewSet)
router.register("homilies", views.HomilyViewSet)
router.register("shop-items", views.ShopItemViewSet)
router.register("constitution-articles", views.ConstitutionArticleViewSet)
router.register("albums", views.AlbumViewSet)
router.register("gallery-images", views.GalleryImageViewSet)

urlpatterns = [
    path("site-settings/", views.SiteSettingsView.as_view(), name="site-settings"),
    path("about-page/", views.AboutPageView.as_view(), name="about-page"),
    path("kinanda-project/", views.KinandaProjectView.as_view(), name="kinanda-project"),
    path("", include(router.urls)),
]
