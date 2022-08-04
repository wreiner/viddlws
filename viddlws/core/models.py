#
#   VIDDLWS
#   Django project which uses youtube-dl to download and serve videos.
#   Copyright (C) 2017 Walter Reiner <walter.reiner@wreiner.at>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import logging
import os
import uuid

from django.db import models, transaction
from django.db.models.signals import post_init, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from viddlws.users.models import User

logger = logging.getLogger(__name__)


class KeyValueSetting(models.Model):
    """
    Key-Value settings model.

    Model is used for settings, look for a key and get the value.

    To help with unset keys a function "get_setting_or_default" is available in
    functions.py which should not be needed anymore starting with Django 4.0.
    """

    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.key}: {self.value}"


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class VideoStatus(models.Model):
    """
    Core Video status model.

    Holds string representation of Video statuses.

    Known video statuses are:
    - new
    - downloaded
    - done
    - inprogress
    """

    status = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.status


class Video(models.Model):
    """
    Core Video model.

    Manages information about all Video objects known to the system.
    """

    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#uuidfield
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    modification_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=140)
    titleslug = models.SlugField(unique=True, max_length=140, blank=True)
    url = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, blank=True)
    audio_only = models.BooleanField(default=False)
    extract_audio = models.BooleanField(default=False)
    status = models.ForeignKey(VideoStatus, on_delete=models.CASCADE)
    original_data = models.JSONField(default=dict, blank=True)
    tags = TaggableManager(through=UUIDTaggedItem)

    def save(self, *args, **kwargs):
        """
        Custom save method for the Video object.

        It calls the download_video Celery task on transaction commit when the
        Video status is "new".
        """

        # https://stackoverflow.com/a/53901543
        from .tasks import download_video

        # http://stackoverflow.com/questions/837828/how-do-i-create-a-slug-in-django
        self.titleslug = slugify(self.title)
        super().save(*args, **kwargs)

        if self.status == VideoStatus.objects.get(status="new"):
            transaction.on_commit(lambda: download_video.delay(self.id))

    def set_download_directory_path(self):
        """
        Reads the value for "video_download_dir" from the KeyValueSetting table.

        It uses the "get_setting_or_default" function which should not be needed
        anymore starting with Django 4.0.
        """

        from viddlws.core.functions import get_setting_or_default

        self.download_directory_path = get_setting_or_default(
            "video_download_dir", "/tmp"
        )

    def thumbnailfile(self):
        """
        Depending on the status of the Video object the corresponding thumbnail
        filename will be returned.

        When status is new or inprogress the inprogress thumbnail filename is
        returned, when status is downloaded the function checks the downloads
        directory for the thumbnail file with the extensions jpg, png and webp.
        If such a file is found that files filename will be returned.

        In all other cases a placeholder thumbnail filename will be returnd.

        Returns:
            str: Thumbnail filename for Video object.
        """

        if self.status == VideoStatus.objects.get(status="downloaded"):
            name, extension = os.path.splitext(self.filename)
            for check_extension in ("jpg", "png", "webp"):
                if os.path.exists(
                    f"{self.download_directory_path}/{name}.{check_extension}"
                ):
                    return f"{name}.{check_extension}"

        if self.status in (
            VideoStatus.objects.get(status="new"),
            VideoStatus.objects.get(status="inprogress"),
        ):
            return "inprogress.jpg"

        return "placeholder-thumbnail.jpg"

    def audiofile(self):
        name, extension = os.path.splitext(self.filename)
        return "%s.mp3" % (name)

    def audiotype(self):
        name, extension = os.path.splitext(self.audiofile())
        if extension == ".mp3":
            extension = ".mpeg"
        return "audio/%s" % (extension[1:])

    def videotype(self):
        name, extension = os.path.splitext(self.filename)
        return "video/%s" % (extension[1:])

    def tags_display(self):
        # return ', '.join([_.name for _ in self.tags.all()])
        return self.tags.all()

    def __str__(self):
        return f"T: {self.title} | S: {self.status}[{self.url}]"


@receiver(pre_delete, sender=Video)
def delete_video_hook(sender, instance, using, **kwargs):
    """
    Hook which is handling "pre_delete" calls from Django signals.

    It calls the delete_video_files Celery task when a Video object gets deleted.
    """
    # https://stackoverflow.com/a/53901543
    from .tasks import delete_video_files

    delete_video_files.delay(instance.id)


@receiver(post_init, sender=Video)
def post_init_video_hook(sender, instance, **kwargs):
    """
    Hook which is handling "post_init" calls from Django signals.

    It calls the set_download_directory_path for the created Video object to
    initialize the "download_directory_path" object property.
    """
    instance.set_download_directory_path()
