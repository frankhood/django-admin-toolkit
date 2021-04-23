=====
Usage
=====

To use Django Admin toolkit in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_admin_toolkit.apps.DjangoAdmintoolkitConfig',
        ...
    )

Add Django Admin toolkit's URL patterns:

.. code-block:: python

    from django_admin_toolkit import urls as django_admin_toolkit_urls


    urlpatterns = [
        ...
        url(r'^', include(django_admin_toolkit_urls)),
        ...
    ]
