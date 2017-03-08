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

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from taggit.managers import TaggableManager

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

    user = models.ForeignKey(User)
    title = models.CharField(max_length=140)
    titleslug = models.SlugField(unique=True, max_length=140, blank=True)
    url = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, blank=True)
    audio_only = models.BooleanField(default=False)
    extract_audio = models.BooleanField(default=False)
    status = models.ForeignKey(VideoStatus)
    tags = TaggableManager()

    #FIXME create own save with slugify
    # http://stackoverflow.com/questions/837828/how-do-i-create-a-slug-in-django

    def save(self, *args, **kwargs):
        self.titleslug = slugify(self.title)
        while True:
            try:
                return super(Video, self).save(*args, **kwargs)
            except IntegrityError:
                # generate a new slug
                pass

    def thumbnailfile(self):
        name, extension = os.path.splitext(self.filename)
        return "%s.jpg" % (name)

    def videotype(self):
        name, extension = os.path.splitext(self.filename)
        return "video/%s" % (extension[1:])

    def tags_display(self):
        #return ', '.join([_.name for _ in self.tags.all()])
        return self.tags.all()

    def __str__(self):
        return "T: %s | S: %s[%s]" % (self.title, self.status, self.url)

class KeyValueSetting(models.Model):
    """
    Key-Value settings model
    """

    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return "%s: %s" % (self.key, self.value)

