import os
import sys
from shutil import rmtree

from setuptools import setup, Command


here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds ...')
            rmtree(os.path.join(here, 'dist'))
        except Exception:
            pass

        self.status('Building Source distribution ...')
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))
        self.status('Uploading the package to PyPI via Twine ...')
        os.system('twine upload --repository devpython-pypi dist/*')
        sys.exit()


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
    zip_safe=True,
    cmdclass={'upload': UploadCommand},
)
