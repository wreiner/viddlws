# ViddlWS

ViddlWS (Video Download Web Service) is a Django project which uses [yt_dlp](https://github.com/yt-dlp/yt-dlp) to archive videos from various sites like YouTube and create podcast feeds from them.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Features

* Download and serve videos from various sites like YouTube
* Extract audio or store only audio data from the sources
* Tag the downloaded items
* Subscribe to a podcast feed of tagged items

## Documentation

The documentation can be found in the docs folder.

## Quick start

```
# Clone the repository
git clone https://github.com/wreiner/viddlws
cd viddlws

# Create the config files based on the supplied examples
mkdir -p .envs/.production
cp envfiles-examples/.django-example .envs/.production/.django
cp envfiles-examples/.postgres-example .envs/.production/.postgres

# Set the SECRET_ID
SECRET_ID=$(python3 -c "import secrets; print(secrets.token_urlsafe())")
sed -i "s/<generate-key>/${SECRET_ID}/" .envs/.production/.django

# Set the admin url
ADMIN_URL=$(echo $RANDOM | md5sum | head -c 32; echo;)
sed -i "s/<generate-url>/${ADMIN_URL}\//" .envs/.production/.django

# set the domain
sed -i "s/domain.com/my.fqdn.com/" .envs/.production/.django

# set the flower password
FLOWER_PASSWORD=$(echo $RANDOM | md5sum | head -c 32; echo;)
sed -i "s/<set-password>/${FLOWER_PASSWORD}/" .envs/.production/.django

# set the email configuration in .envs/.production/.django

# set the postgres password
POSTGRES_PASSWORD=$(echo $RANDOM | md5sum | head -c 32; echo;)
sed -i "s/<set-password>/${POSTGRES_PASSWORD}/" .envs/.production/.postgres

# make sure that the downloads directory exists
sudo mkdir -p /viddlws/downloads
sudo chown 101: /viddlws/downloads/

# startup ViddlWS for the first time
docker-compose -f production-behind-proxy.yml pull
docker-compose -f production-behind-proxy.yml up

# the initial admin user password will be echo'ed in the django container logs
docker logs viddlws_django_1 2>&1| grep "New admin password:"

# change site domain in admin gui
# open https://my.fqdn.com/${ADMIN_URL}/
# navigate to Sites and change domain.com entry
```
