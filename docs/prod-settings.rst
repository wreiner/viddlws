 .. _prod-settings:

Settings for Production Deployment
======================================================================

The most common settings can be configured through env files.

Examples for those files can be found in `envfiles-examples/`.

* for Django the file is `envfiles-examples/.django-example`
* for PostgreSQL the file is `envfiles-examples/.postgres-example`

Most settings should be pretty self explainatory.

Replace all occurences of values that start and end with: `<>`
For an example on how to set these values refer to :ref:`quick-start`.

For settings which are not
widely known see the following table for an explaination:

===========================         =====
Setting                             What it is used for
===========================         =====
DJANGO_SECRET_KEY                   Used to provide cryptographic signing

                                    https://docs.djangoproject.com/en/stable/ref/settings/#secret-key
DJANGO_ADMIN_URL                    URL path to admin interface, normally /admin
DJANGO_ALLOWED_HOSTS                FQDN of your ViddlWS installation
===========================         =====

Probably the most important setting is `DJANGO_SECRET_KEY`.

To generate such a secret key run:

.. code-block:: bash

    python -c "import secrets; print(secrets.token_urlsafe())"

=======================
Initial admin password
=======================

On the first start of the Django docker container an initial admin password
will be generated and echo'ed into the logs.

Please change the password as soon as possible.

At the time of writing it is not yet possible to set the initial admin password
manually.

================
Downloads volume
================

No matter if ViddlWS is running behind a proxy or public facing, videos need to
be downloaded onto a local disk. To pass the disk to the docker containers add
the respective host-path to the volumes for the services which need access to
this volume.

Default host-path is `/viddlws/downloads`.

The django containers use UID/GID of 101 so set the permissions accordingly:

.. code-block:: bash

    sudo chown 101:101 /viddlws/downloads

If the download path should be different, replace this value with the value of
choice in the docker-compose files. For further information see the Docker
documentation regarding bind mounts.
