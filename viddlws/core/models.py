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

import os
import uuid

from django.db import IntegrityError, models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from viddlws.users.models import User


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class VideoStatus(models.Model):
    """
    Video status

    - new
    - downloaded
    - done
    """

    status = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.status


class Video(models.Model):
    """
    Download(ed) Videos mangement
    """

    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#uuidfield
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    titleslug = models.SlugField(unique=True, max_length=140, blank=True)
    url = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, blank=True)
    audio_only = models.BooleanField(default=False)
    extract_audio = models.BooleanField(default=False)
    status = models.ForeignKey(VideoStatus, on_delete=models.CASCADE)
    tags = TaggableManager(through=UUIDTaggedItem)

    # FIXME create own save with slugify
    # http://stackoverflow.com/questions/837828/how-do-i-create-a-slug-in-django

    def save(self, *args, **kwargs):
        self.titleslug = slugify(self.title)
        while True:
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                # generate a new slug
                pass

    def thumbnailfile(self):
        name, extension = os.path.splitext(self.filename)
        return "%s.jpg" % (name)

    def audiofile(self):
        name, extension = os.path.splitext(self.filename)
        return "%s.mp3" % (name)

    def audiotype(self):
        name, extension = os.path.splitext(self.audiofile())
        return "audio/%s" % (extension[1:])

    def videotype(self):
        name, extension = os.path.splitext(self.filename)
        return "video/%s" % (extension[1:])

    def tags_display(self):
        # return ', '.join([_.name for _ in self.tags.all()])
        return self.tags.all()

    def __str__(self):
        return f"T: {self.title} | S: {self.status}[{self.url}]"


class KeyValueSetting(models.Model):
    """
    Key-Value settings model
    """

    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.key}: {self.value}"
