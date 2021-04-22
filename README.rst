=============================
Django Admin Utils
=============================

.. image:: https://badge.fury.io/py/django-admin-utils.svg
    :target: https://badge.fury.io/py/django-admin-utils

.. image:: https://travis-ci.org/frankhood/django-admin-utils.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-admin-utils

.. image:: https://codecov.io/gh/frankhood/django-admin-utils/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-admin-utils

A set of mixins and methods to simplify the Django Admin development

Documentation
-------------

The full documentation is at https://django-admin-utils.readthedocs.io.

Quickstart
----------

Install Django Admin Utils::

    pip install django-admin-utils

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_admin_utils.apps.DjangoAdminUtilsConfig',
        ...
    )

Add Django Admin Utils's URL patterns:

.. code-block:: python

    from django_admin_utils import urls as django_admin_utils_urls


    urlpatterns = [
        ...
        url(r'^', include(django_admin_utils_urls)),
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
