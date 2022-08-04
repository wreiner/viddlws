 .. _core:

Core
======================================================================

At the time of writing all functionality is implemented in the Core app.

Mostly class based views are used.

* Celery tasks are implemented in viddlws.core.tasks
* RSS feed functions are implemented in viddlws.core.feeds
* Helper functions are located in viddlws.core.functions

=================
Models
=================

.. automodule:: viddlws.core.models
   :members:
   :noindex:

=================
CBV Forms
=================

.. automodule:: viddlws.core.forms
   :members:
   :noindex:

=================
Helper Functions
=================

.. automodule:: viddlws.core.functions
   :members:
   :noindex:

=======================
Celery tasks functions
=======================

.. automodule:: viddlws.core.tasks
   :members:
   :noindex:
   :undoc-members:
   :show-inheritance:

   .. autofunction:: download_video(video_id)
   .. autofunction:: delete_video_files(video_id)

====================
RSS Feed Generation
====================

.. automodule:: viddlws.core.feeds
   :members:
   :noindex:
