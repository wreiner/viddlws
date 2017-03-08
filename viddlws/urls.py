"""viddlws URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from core.views import VideoListView
from core.views import TagListView
from core.views import VideoCreate
from core.views import VideoUpdate
from core.views import VideoDelete
from core.views import VideoDetail

urlpatterns = [
    # core
    url(r'^$',  VideoListView.as_view(),),
    url(r'^v/(?P<pk>[\d]+)/$',  VideoDetail.as_view(),),
    url(r'^add_video/$',  VideoCreate.as_view(),),

    url(r'^tags/$',  TagListView.as_view(),),
    url(r'^tags/(?P<slug>[-\w]+)/$',  VideoListView.as_view(),),

    url(r'^admin/', admin.site.urls),

    # User login|logout
    url('^', include('django.contrib.auth.urls')),
]
