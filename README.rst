
DRF Coupons
-----------

A django-rest-framework application that provides many varieties of coupons

Detailed documentation is in the README.md file.

Quick start
-----------

1. Add "coupons" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'coupons',
    ]

2. Include the coupons URLconf in your project urls.py like this::

    url(r'^', include('coupons.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

