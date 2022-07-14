from django.conf.urls import url

from viddlws.core.views import TagListView, VideoCreate, VideoDetail, VideoListView

app_name = "core"
urlpatterns = [
    # core
    url(
        r"^$",
        VideoListView.as_view(),
    ),
    url(
        r"^v/(?P<pk>[\d]+)/$",
        VideoDetail.as_view(),
    ),
    url(
        r"^add_video/$",
        VideoCreate.as_view(),
    ),
    url(
        r"^tags/$",
        TagListView.as_view(),
    ),
    url(
        r"^tags/(?P<slug>[-\w]+)/$",
        VideoListView.as_view(),
    ),
]
