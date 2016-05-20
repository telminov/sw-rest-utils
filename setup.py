# coding: utf-8
# python setup.py sdist register upload
from setuptools import setup

setup(
    name='sw-rest-utils',
    version='0.0.4',
    description='Soft Way company REST utils.',
    author='Telminov Sergey',
    url='https://github.com/telminov/sw-rest-utils',
    packages=[
        'sw_rest_utils',
    ],
    include_package_data=True,
    license='The MIT License',
    install_requires=[
        'requests',
        'djangorestframework',
        'sw-django-utils',
    ],
)
