# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='yandex_disk_client',
    version='0.0.1',
    packages=[
        'yandex_disk_client',
    ],
    package_data={
        '': ['README.txt'],
    },
    requires=[
        'requests==2.18'
    ]
)
