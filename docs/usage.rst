=====
Usage
=====

To use Django Admin Toolkit in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'admin_toolkit.apps.AdminToolkitConfig',
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
