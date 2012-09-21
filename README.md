django-shipping
===============

Django Shipping is a django application that provides integration with Correios (federal brazilian carrier) and UPS (international carrier).


## Installation and Usage

Anyway, let's install this bitch! The first thing you'll want to do is run:

``` bash
$ pip install django-shipping
```

Next, put `shippging`` in your ``INSTALLED_APPS``:

``` python
# settings.py

INSTALLED_APPS = (
    # ...
    'shipping',
)

```

Now, you need to run shipping migrations. We use south for this, go to your project dir and make:

``` bash
$ pip manage.py migrate shipping
```
