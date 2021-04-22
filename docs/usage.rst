=====
Usage
=====

To use Django Admin Utils in a project, add it to your `INSTALLED_APPS`:

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
