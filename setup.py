import os
from setuptools import setup


def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('shipping'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

setup(name='shipping',
    version='0.0.1',
    description='Django shipping tool',
    author=u'Marcel Nicolay',
    author_email='marcelnicolay@gmail.com',
    url='http://github.com/marcelnicolay/django-shipping',
    install_requires=['Django'],
    packages=get_packages(),
)
