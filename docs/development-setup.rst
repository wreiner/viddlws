 .. _development-setup:

Development Setup And Tipps
======================================================================

Development is done with Docker.

To build the containers run:

.. code-block:: bash

  docker-compose -f local.yml build

To start the local environment run:

.. code-block:: bash

  docker-compose -f local.yml up

To start the documentation server run:

.. code-block:: bash

  docker-compose -f local.yml up docs

After starting the environment create a database schema:

.. code-block:: bash

  docker-compose -f local.yml run --rm django python manage.py migrate

To create a **superuser account**, use this command:

.. code-block:: bash

  docker-compose -f local.yml run --rm django python manage.py createsuperuser

To prefill the VideoStatus and KeyValueSettings tables run:

.. code-block:: bash

  docker-compose -f local.yml run --rm django python manage.py loaddata --app core VideoStatus.json
  docker-compose -f local.yml run --rm django python manage.py loaddata --app core KeyValueSettings.json

=================
pre-commit hooks
=================

This project uses pre-commit hooks configured in `.pre-commit-config.yaml`.

To install the scripts run:

.. code-block:: bash

  pre-commit install

==============
Test coverage
==============

To run the tests, check your test coverage, and generate an HTML coverage report:

.. code-block:: bash

  docker-compose -f local.yml run --rm django run -m pytest
  docker-compose -f local.yml run --rm django coverage report
  docker-compose -f local.yml run --rm django coverage html

==============================
Serve static files with nginx
==============================

An example nginx config block could look like this:

.. code-block:: bash

  server {
      server_name  devviddlws.example.com;

      location / {
          proxy_pass   http://127.0.0.1:8000;
      }

      location /downloads/ {
          autoindex on;
          alias /viddlws/downloads/;
      }
  }
