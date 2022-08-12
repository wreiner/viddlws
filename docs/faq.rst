 .. _faq:

Frequently Asked Questions And Tipps
======================================================================

====================
Lost admin password
====================

If you have lost your admin password the easiest solution is to create a second
admin user, login with it and reset passwords of users:

.. code-block:: bash

    docker-compose -f production-behind-proxy.yml run --rm django python manage.py createsuperuser

====================
Recode video to mp4
====================

To recode a video file into .mp4 with ffmpeg:

.. code-block:: bash

    ffmpeg -i <input-file.ext> -c:v libx264 -c:a aac <output-file>.mp4

