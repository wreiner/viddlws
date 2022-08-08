 .. _quick-start:

Quick Start
======================================================================

.. code-block:: bash

    # Clone the repository
    git clone
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

    # set the postgres password
    POSTGRES_PASSWORD=$(echo $RANDOM | md5sum | head -c 32; echo;)
    sed -i "s/<set-password>/${POSTGRES_PASSWORD}/" .envs/.production/.postgres

    # make sure that the downloads directory exists
    sudo mkdir -p /viddlws/downloads

    # startup ViddlWS for the first time
    docker-compose -f production-behind-proxy.yml pull
    docker-compose -f production-behind-proxy.yml up

    # change site domain in admin gui
    # open https://my.fqdn.com/${ADMIN_URL}/
    # navigate to Sites and change domain.com entry
