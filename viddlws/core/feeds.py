import os

import sesame.utils
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import feedgenerator

from viddlws.core.functions import get_setting_or_default
from viddlws.users.models import User

from .models import Video


class MediaFeed(Feed):
    def _get_filesize_in_bytes(self, filepath):
        file_stats = os.stat(filepath)
        return file_stats.st_size

    def get_object(self, request, slug):
        user = sesame.utils.get_user(request)
        return {"slug": slug, "fullpath": request.get_full_path(), "user": user}

    def title(self, obj):
        return "Tag '{}' - VIDDLWS feed".format(obj.get("slug"))

    def link(self, obj):
        return obj.get("fullpath")

    def description(self, obj):
        return "VIDDLWS feed of all entries for tag {}".format(obj.get("slug"))

    def items(self, obj):
        user = User.objects.get(username=obj.get("user"))
        if not user:
            return None

        return (
            Video.objects.filter(
                user=user, status__status="downloaded", tags__slug=obj.get("slug")
            )
            .exclude(tags__name__in=["xxx", "private"])
            .order_by("-modification_date")
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.original_data.get("description")

    def item_link(self, item):
        return reverse("video", kwargs={"object_pk": item.pk})

    def item_enclosures(self, item):
        # FIXME add host part, always replace extension with mp3?
        enc_url = item.filename

        filepath = "{}/{}".format(
            get_setting_or_default("video_download_dir", "/tmp"), item.filename
        )

        if enc_url:
            enc = feedgenerator.Enclosure(
                url=str(enc_url),
                length=str(self._get_filesize_in_bytes(filepath)),
                mime_type="audio/mpeg",
            )
            return [enc]
        return []