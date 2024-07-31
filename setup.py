#!/usr/bin/env python


from setuptools import setup


setup(
    name='meter_suite',
    version='1.0',
    description='Meter reading and archiving suite for EKM meters. Intended to be run on Rasbperry Pi, Andino X1 platform.',
    author='Vitaly Greck',
    author_email='vintozver@ya.ru',
    url='https://www.python.org/sigs/distutils-sig/',
    package_dir={'meter_suite': 'src'},
    install_requires=[
        'jinja2', 'python_dateutil', 'ekmmeters'
    ],
)
