.. Parker documentation master file, created by
   sphinx-quickstart on Wed Jun 13 14:41:22 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Parker's documentation!
==================================

Parker is designed to make realtime publishing from django easy. It puts marimo_ widgets in pages and communicates with them via browsermq_ 

The main work of publishing with parker is in defining carriers. These carriers determine what will be published to what queues and also can be used to add widgets to pages with the templatetag. Each carrier should usually contain all of the publishing information for a given widget. These carriers can be used by more than one widget that consume the same information by passing different templates or widget prototypes to the template tag. A listener for each type of information a carrier will handle should be set up too.


Getting started
________________
TODO fix this when setting it up somewhere new

* You will need to get browsermq_ running somewhere.
* make django server serve required javascript for widgets
* set settings_.
* `django-admin.py runserver --settings=parker_demo.settings`

.. _marimo: http://github.com/coxmediagroup/marimo
.. _browsermq: http://github.com/coxmediagroup/parker
.. _settings: settings

Contents:

.. toctree::
   :maxdepth: 2

   carriers
   listeners
   settings
   templatetag


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

