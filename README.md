# viddlws
Django project which uses youtube-dl to download and serve videos.

## Installation

### Development

- Generate secret key in settings.py
- Install requirements
```
pip3 install -r requirements.txt
```
- Configure database settings in settings.py
- Migrate database
```
python manage.py migrate
```
- Load initial database setup
```
python manage.py loaddata core/fixtures/KeyValueSettings.json
python manage.py loaddata core/fixtures/VideoStatus.json
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
- Change download dir setting in Django Admin interface to Core.KeyValueSetting, e.g.
```
video_download_dir: /usr/share/viddlws/downloads
```

### Production

The use of the build-in development server is discouraged for productional use.

A set of example configuration and systemd unit files can be found in the install directory.

In development environments the Django development server serves all static contents. In
production environments this is not the case. All static content needs to be collected into a single
directory. This diretory is configured through Django settings.py with the _STATIC_ROOT_ directive:

```
STATIC_ROOT = "/usr/share/viddlws/static"
```

To gather the files into the STATIC_ROOT directory run:

```
python manage.py collectstatic
```



## Screenshots

![Video Overview](https://github.com/wreiner/viddlws/blob/master/screenshots/viddlws-video_overview.png)

![Adding Video](https://github.com/wreiner/viddlws/blob/master/screenshots/viddlws-add-video.png)

![Video Details](https://github.com/wreiner/viddlws/blob/master/screenshots/viddlws-video-detail.png)
