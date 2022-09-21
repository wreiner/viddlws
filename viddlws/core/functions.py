import shutil

from viddlws.core.models import KeyValueSetting


# FIXME not needed in Django 4.0
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/#default
def get_setting_or_default(key, default_value):
    """
    Helper function which reads a key-value pair from the KeyValueSetting model.

    If the key-value pair is not found the supplied default value is returned.

    This function should not be needed anymore starting with Django 4.0.
    """
    obj = None
    try:
        obj = KeyValueSetting.objects.get(key=key)
    except KeyValueSetting.DoesNotExist:
        print("%s not set, using default" % (key))
        return default_value
    except KeyValueSetting.MultipleObjectsReturned:
        print("%s set multiple times, using default" % (key))
        return default_value
    else:
        return obj.value


def get_download_filesystem_usage(download_directory):
    total, used, free = shutil.disk_usage(download_directory)

    total = f"{total/float(1<<30):,.0f}"
    used = f"{used/float(1<<30):,.0f}"
    free = f"{free/float(1<<30):,.0f}"
    percent_used = f"{int(used) * 100 / int(total):,.0f}"

    return {"total": total, "used": used, "free": free, "percent_used": percent_used}
