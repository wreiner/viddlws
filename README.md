# viddlws
Django project which uses youtube-dl to download and serve videos.

## Installation

### Development

- Generate secret key in settings.py
- Configure database settings in settings.py
- Migrate database
```
python manage.py migrate
```
- Create superuser
```
python manage.py createsuperuser
```
- Add sites DNS domain to settings.py
- Run development server
```
python manage.py runserver 0.0.0.0:8001
```
- Add download dir setting in Django Admin interface to Core.KeyValueSetting, e.g.
```
video_download_dir: /usr/share/viddlws/downloads
```

### Production

The use of the build-in development server is discouraged for productional use.

## Screenshots

![Video Overview](https://github.com/wreiner/viddlws/blob/master/screenshots/viddlws-video_overview.png)

![Adding Video](https://github.com/wreiner/viddlws/blob/master/screenshots/viddlws-add-video.png)

![Video Details](https://github.com/wreiner/viddlws/blob/master/screenshots/viddlws-video-detail.png)
