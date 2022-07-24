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

from django.forms import ModelForm

from .models import Video


class VideoAddForm(ModelForm):
    class Meta:
        model = Video

        # http://stackoverflow.com/a/28306347
        #   set fields list or __all__
        # or exclude fields with a tuple
        # http://stackoverflow.com/a/8139277
        #   exclude = ('created_by',)
        exclude = (
            "user",
            "status",
            "filename",
            "titleslug",
            "original_data",
        )


class VideoEditForm(ModelForm):
    class Meta:
        model = Video

        # http://stackoverflow.com/a/28306347
        #   set fields list or __all__
        # or exclude fields with a tuple
        # http://stackoverflow.com/a/8139277
        #   exclude = ('created_by',)
        exclude = (
            "user",
            "status",
            "filename",
            "titleslug",
            "original_data",
            "audio_only",
            "extract_audio",
        )
