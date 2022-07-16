# Python imports
import logging
import os
import pathlib
import re

from yt_dlp import YoutubeDL

# Local imports
from config import celery_app
from viddlws.core.functions import get_setting_or_default
from viddlws.core.models import Video, VideoStatus

# Get an instance of the logger
logger = logging.getLogger(__name__)


# FIXME store time only update progress in table in 10 seconds
def ydl_hooks(d):
    if d["status"] == "finished":
        # https://stackoverflow.com/a/14166194
        uuid = re.findall(
            r"^([a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})",
            pathlib.Path(d["filename"]).name,
        )
        if not uuid:
            logger.error("cannot extract uuid from filename {}".format(d["filename"]))
            return

        logger.info(f"got video uuid {uuid} which has just finished downloading ..")

        video = Video.objects.get(id=uuid[0])
        if not video:
            logger.error(f"cannot find video item for id {uuid}")
            return

        video.status = VideoStatus.objects.get(status="downloaded")
        # video.thumbnail_extension = pathlib.Path(d["info_dict"]["thumbnail"].suffix)
        video.filename = pathlib.Path(d["filename"]).name

        # we don't want this information stored
        d["info_dict"]["automatic_captions"] = ""
        d["info_dict"]["formats"] = ""
        d["info_dict"]["thumbnails"] = ""
        video.original_data = d["info_dict"]

        video.save()

        logger.info(f"video uuid {uuid} data updated, all finished ..")


@celery_app.task()
def download_video(video_id):
    video = Video.objects.get(id=video_id)
    if not video:
        logger.info(f"supplied video id {video_id} not found, exiting.")
        return

    # existing_video = Video.objects.get(url=video.url)
    # if existing_video:
    #     video.filename = existing_video.filename
    #     video.status = existing_video.status
    #     return

    video_download_dir = get_setting_or_default("video_download_dir", "/tmp")
    logger.info("got video_download_dir: %s" % (video_download_dir))

    # https://github.com/rg3/youtube-dl/issues/5192#issuecomment-78843396
    # https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L279
    outtmpl = f"{video_download_dir}/{video.id}-{video.titleslug}-%(id)s.%(ext)s"

    ydl_opts = {
        "progress_hooks": [ydl_hooks],
        "outtmpl": outtmpl,
        "quiet": True,
        "restrictfilenames": True,
        "writethumbnail": True,
    }

    if not video.audio_only:
        video_opt_dics = {
            "format": "bestvideo[ext=webm]+bestaudio[ext=mp3]/best",
            # 'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]',
            # 'format': 'bestvideo+bestaudio/best',
        }

        # http://stackoverflow.com/a/26853961/7523861
        ydl_opts = {**video_opt_dics, **ydl_opts}

    if not video.audio_only:
        logger.debug("selected keep video")
        ydl_opts["keepvideo"] = True

    if video.extract_audio:
        logger.debug("selected extract audio")

        # http://stackoverflow.com/a/27481870/7523861
        extract_audio_dict = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        # http://stackoverflow.com/a/26853961/7523861
        ydl_opts = {**extract_audio_dict, **ydl_opts}

    with YoutubeDL(ydl_opts) as ydl:
        logger.info(f"will download {video.title}[{video.url}]")

        info_dict = ydl.extract_info(video.url, download=False)

        # https://github.com/rg3/youtube-dl/issues/5602#issuecomment-121125432
        video.filename = os.path.basename(ydl.prepare_filename(info_dict))
        ydl.download([video.url])
