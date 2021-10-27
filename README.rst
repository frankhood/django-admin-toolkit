=============================
Django Admin Toolkit
=============================

.. image:: https://badge.fury.io/py/django-admin-toolkit.svg/?style=flat-square
    :target: https://badge.fury.io/py/django-admin-toolkit

.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
    :target: https://django-admin-toolkit.readthedocs.io/en/latest/

.. image:: https://img.shields.io/coveralls/github/frankhood/django-admin-toolkit/master?style=flat-square
    :target: https://coveralls.io/github/frankhood/django-admin-toolkit?branch=master
    :alt: Coverage Status

Multiple admin mixin for yours Django Admins

Documentation
-------------

The full documentation is at https://django-admin-toolkit.readthedocs.io.

Quickstart
----------

Install Django Admin Toolkit::

    pip install django-admin-toolkit

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'admin_toolkit',
        ...
    )

Add Django Admin Toolkit's URL patterns:

.. code-block:: python

    from admin_toolkit import urls as admin_toolkit_urls


    urlpatterns = [
        ...
        url(r'^', include(admin_toolkit_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
