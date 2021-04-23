=============================
Django Admin toolkit
=============================

.. image:: https://badge.fury.io/py/django-admin-toolkit.svg
    :target: https://badge.fury.io/py/django-admin-toolkit

.. image:: https://travis-ci.org/frankhood/django-admin-toolkit.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-admin-toolkit

.. image:: https://codecov.io/gh/frankhood/django-admin-toolkit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-admin-toolkit

Overview
-------------

A set of mixins and methods to simplify the Django Admin development

Quickstart
----------

Install Django Admin toolkit::

    pip install django-admin-toolkit


Add it to your `INSTALLED_APPS`:

::

    INSTALLED_APPS = (
        ...
        'django_admin_toolkit',
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
