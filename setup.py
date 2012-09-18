from setuptools import setup


setup(
    name='shipping',
    version='0.0.1',
    description='Django shipping tool',
    long_description=open("README.md").read(),
    author=u'Marcel Nicolay',
    author_email='marcelnicolay@gmail.com',
    url='http://github.com/marcelnicolay/django-shipping',
    install_requires=open("requirements.txt").read().split("\n"),
    packages=['shipping'],
)
