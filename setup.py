from setuptools import setup

setup(
    name='yandex_disk_client',
    version='0.0.2',
    author='Dmitry Burnaev',
    license='MIT',
    packages=[
        'yandex_disk_client',
    ],
    package_data={
        '': ['README.md', 'LICENSE'],
    },
    install_requires=[
       'requests==2.21'
    ],
)
