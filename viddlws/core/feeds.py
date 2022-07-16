import os

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import feedgenerator

from viddlws.core.functions import get_setting_or_default

from .models import Video


class DreamrealCommentsFeed(Feed):
    title = "Dreamreal's comments"
    link = "/drcomments/"
    description = "Updates on new comments on Dreamreal entry."

    def _get_filesize_in_bytes(self, filepath):
        file_stats = os.stat(filepath)
        return file_stats.st_size

    def items(self):
        return Video.objects.all().order_by("-modification_date")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # return dict(item.original_data).get("description")
        return item.original_data.get("description")

    def item_link(self, item):
        return reverse("video", kwargs={"object_pk": item.pk})

    def item_enclosures(self, item):
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
