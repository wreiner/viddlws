#!/usr/bin/env python
#
#   VIDDLWS downloader
#   Downloads videos for VIDDLWS.
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

#
# http://stackoverflow.com/questions/8047204/django-script-to-access-model-objects-without-using-manage-py-shell
#

from __future__ import unicode_literals
import sys
import os
import logging
import re
import pprint

sys.path.append('/usr/share/viddlws')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "viddlws.settings")

import youtube_dl
import django
django.setup()

from core.models import *

# Get an instance of the logger
logger = logging.getLogger(__name__)

CURVID = None

def get_setting_or_default(key, default_value):
    obj = None
    try:
        obj = KeyValueSetting.objects.get(key=key)
    except KeyValueSetting.DoesNotExist as e:
        print("%s not set, using default" % (key))
        return default_value
    except KeyValueSetting.MultipleObjectsReturned as e:
        print("%s set multiple times, using default" % (key))
        return default_value
    else:
        return obj.value

#FIXME store time only update progress in table in 10 seconds
def ydl_hooks(d):
    print("got the following value: %s" % (d))

    if d["status"] == "finished":
        CURVID.status = VideoStatus.objects.get(status="downloaded")
        CURVID.save()

if __name__ == '__main__':
    video_download_dir = get_setting_or_default("video_download_dir", "/tmp")
    print("got video_download_dir: %s" % (video_download_dir))

    videos_to_download = Video.objects.filter(status__status="new")
    if not videos_to_download:
        print("no videos to download, exiting")
        sys.exit(0)

    for video in videos_to_download:
        CURVID = video

        # https://github.com/rg3/youtube-dl/issues/5192#issuecomment-78843396
        # https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L279
        outtmpl = "%s/%s-%%(id)s.%%(ext)s" % (video_download_dir, video.titleslug)

        ydl_opts = {
                'progress_hooks': [ydl_hooks],
                'outtmpl': outtmpl,
                'quiet': True,
                'restrictfilenames': True,
                'writethumbnail': True,
            }

        if not video.audio_only:
            video_opt_dics = {
                'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]',
            }

            # http://stackoverflow.com/a/26853961/7523861
            ydl_opts = {**video_opt_dics, **ydl_opts}

        if not video.audio_only:
            print("selected keep video")
            ydl_opts["keepvideo"] = True

        if video.extract_audio:
            print("selected extract audio")

            # http://stackoverflow.com/a/27481870/7523861
            extract_audio_dict = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            # http://stackoverflow.com/a/26853961/7523861
            ydl_opts = {**extract_audio_dict, **ydl_opts}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("will download %s[%s]" % (video.title, video.url))

            info_dict = ydl.extract_info(video.url, download=False)

            # https://github.com/rg3/youtube-dl/issues/5602#issuecomment-121125432
            video.filename = os.path.basename(ydl.prepare_filename(info_dict))
            ydl.download([video.url])

            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(info_dict)
