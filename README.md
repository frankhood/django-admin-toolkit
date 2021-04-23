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

Features
--------

* EmptyValueMixinAdmin find another way to change the empty label
* Complete testing of admin mixins
* Add unit tests

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
