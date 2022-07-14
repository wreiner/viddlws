from django.contrib import admin

from .models import KeyValueSetting, Video, VideoStatus

admin.site.register(Video)
admin.site.register(VideoStatus)
admin.site.register(KeyValueSetting)
