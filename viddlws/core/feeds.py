import os

import sesame.utils
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.urls import reverse
from django.utils import feedgenerator

from viddlws.core.functions import get_setting_or_default
from viddlws.users.models import User

from .models import Video


class MediaFeed(Feed):
    """
    Feed class to provide data for RSS feed
    """

    def get_context_data(self, **kwargs):
        setattr(
            self, "request", kwargs["request"]
        )  # to access the request object later
        return super().get_context_data(**kwargs)

    def _get_filesize_in_bytes(self, filepath):
        """
        Podcast feeds need the filesize.
        """
        file_stats = os.stat(filepath)
        return file_stats.st_size

    def get_object(self, request, slug):
        """
        Handle user provided data.
        """
        user = sesame.utils.get_user(request)
        return {
            "slug": slug,
            "fullpath": request.get_full_path(),
            "user": user,
            "audio_only": request.GET.get("audio_only"),
        }

    def title(self, obj):
        """
        Creates the overall feed title.
        """
        return "{} - VIDDLWS tag feed".format(obj.get("slug"))

    def link(self, obj):
        """
        Creates the overall feed link.
        """
        return obj.get("fullpath")

    def description(self, obj):
        """
        Creates the overall feed description.
        """
        return "VIDDLWS feed of all entries for tag {}".format(obj.get("slug"))

    def items(self, obj):
        """
        Returns the actual items which should appear in the feed per authenticated user.

        If audio_only is set by the user the filter will only list audio items.

        Special tag categories will not be included in the feed.
        """
        user = User.objects.get(username=obj.get("user"))
        if not user:
            return None

        query_filter = Q()
        query_filter.add(
            Q(user=user)
            & Q(status__status="downloaded")
            & Q(tags__slug=obj.get("slug")),
            Q.AND,
        )

        if obj.get("audio_only"):
            query_filter.add((Q(audio_only=True) | Q(extract_audio=True)), Q.AND)

        return (
            Video.objects.filter(query_filter)
            .exclude(tags__name__in=["xxx", "private"])
            .order_by("-modification_date")
        )

    def item_title(self, item):
        """
        Returns the title of the feed item.
        """
        return item.title

    def item_description(self, item):
        """
        Returns the description of the feed item.

        Here the original description from the source is returned.
        """
        return item.original_data.get("description")

    def item_link(self, item):
        """
        Returns the direct link of the feed item media file.
        """
        return reverse("v", kwargs={"pk": item.pk})

    def item_enclosures(self, item):
        """
        Returns the enclosure element for the item in the feed.
        """

        # set standard mime_type
        mime_type = "audio/mpeg"
        if item.audio_only or item.extract_audio:
            current_site = Site.objects.get_current()
            mime_type = item.audiotype()
            item.filename = item.audiofile()
        else:
            mime_type = item.videotype()

        enc_url = (
            f"{self.request.scheme}://{current_site.domain}/downloads/{item.filename}"
        )
        filepath = "{}/{}".format(
            get_setting_or_default("video_download_dir", "/tmp"), item.filename
        )

        if enc_url:
            enc = feedgenerator.Enclosure(
                url=str(enc_url),
                length=str(self._get_filesize_in_bytes(filepath)),
                mime_type=mime_type,
            )
            return [enc]
        return []
