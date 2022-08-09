 .. _public-facing:

Public facing ViddlWS
======================================================================

To deploy ViddlWS public facing and not behind a reverse proxy or a loadbalancer
the docker-compose file production.yml in the repository can be used.

To obtain a Let's Encrypt certificate you have to change the traefik configuration
in `compose/production/traefik/traefik.yml`:

=========   ====================
Change      What it is used for
=========   ====================
email       Let's Encrypt registration email address
rule        domain for which the certificate should be issued, replace all *domain.com occurences
=========   ====================

After changing the values build the images:

.. code-block:: bash

    docker-compose production.yml build

Before starting the containers please also follow the common :ref:`prod-settings`
documentation.

To start the containers run:

.. code-block:: bash

    docker-compose production.yml up

This has not been tested and likely will need additional work.
