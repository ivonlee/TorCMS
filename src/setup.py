#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='torcms',
    version='0.0.8',
    keywords=('torcms', 'tornado', 'cms',),
    description='''CMS based on Python 3 and Tornado.
        Flexible, extensible web CMS framework built on Tornado, Peewee and Purecss, compatible with Python 3.4 and 3.5.
        ''',
    license='MIT License',

    url='https://github.com/bukun/TorCMS',
    # download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', #
    author='bukun',
    author_email='bukun@osgeo.cn',

    # packages=find_packages(exclude=["ext*", "torapp_ext"]),
    packages=find_packages(exclude=["maplet.*", "maplet"]),

    # packages=find_packages(exclude=["maplet"]),
    # package_data=find_package_data(
    # 	PACKAGE,
    # 	only_in_packages=False
    #  ),
    # include_package_data=True,
    # exclude_package_data={'': ['*maplet*']},
    platforms='any',
    zip_safe=True,
    install_requires=['beautifulsoup4', 'jieba', 'markdown', 'peewee', 'Pillow',
        'tornado', 'Jinja2', 'Whoosh', 'WTForms', 'wtforms-tornado','psycopg2'],

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
