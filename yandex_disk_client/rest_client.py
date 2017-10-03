from urllib.parse import urljoin

from requests import request

from .core import Directory, Disk, File
from .exceptions import YaDiskInvalidStatusException, \
    YaDiskInvalidResultException

BASE_URL = "https://cloud-api.yandex.net:443/v1/disk"


class YandexDiskClient(object):
    """
    Implementation of https://tech.yandex.ru/disk/poligon/
    """
    _base_url = BASE_URL

    def __init__(self, token):
        self.token = token

        self.base_headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + self.token,
            "Host": "cloud-api.yandex.net"
        }

    def request(self, method, url, **kwargs):
        resp = request(method, url, headers=self.base_headers, **kwargs)
        if resp.status_code not in [200, 201]:
            raise YaDiskInvalidStatusException(resp.status_code, resp.text)

        resp_data = resp.json()
        if resp_data.get('status') != 'ok':
            raise YaDiskInvalidResultException(url, resp_data.get('status'))

        return resp_data

    def get_disk_metadata(self):
        """
        :return: disk metadata
        """
        disk_info = self.request('get', self._base_url)
        return Disk(**disk_info)

    def get_directory(self, path):
        """
        :param path: path to folder
        :return: content of folder
        """
        url = urljoin(self._base_url, 'resources')
        directory_info = self.request('get', url, params={'path': path})
        return Directory(**directory_info)

    def mkdir(self, path):
        """
        :param path: path to folder
        :return: created folder
        """
        url = urljoin(self._base_url, 'resources')
        result_info = self.request('put', url, params={'path': path})
        # TODO: need to check result info!!
        return self.get_directory(path)

    def remove(self, path):
        """ Remove file or directory (by path) """

        url = urljoin(self._base_url, 'resources')
        result_info = self.request('delete', url, params={'path': path})
        # TODO: need to check result info!!
        return result_info

    def copy(self, path_from, path_to):
        """ Copy file or directory """

        url = urljoin(self._base_url, 'resources/copy')
        payload = {'path': path_to, 'from': path_from}
        result_info = self.request('post', url, params=payload)
        return result_info

    def get_download_link_to_file(self, path_to_file):
        """
        Create Yandex download link
        :return: ???
        """

        url = urljoin(self._base_url, 'resources/download')
        result_info = self.request('get', url, params={'path': path_to_file})
        # TODO: need to check result info!!
        return result_info

    def get_published_elements(self):
        """
        :return: published elements
        """
        json_dict = self._get_published_files()

        elements = []

        for item in json_dict["items"]:
            if item["type"] == "dir":
                elements.append(Directory(**item))
            elif item["type"] == "file":
                elements.append(File(**item))

        return elements

    def publish(self, path):
        """get public link to folder or file
        :param path: path to publication file or directory
        :return: public link to folder or file
        """

        url = urljoin(self._base_url, 'resources/publish')
        result_info = self.request('put', url, params={'path': path})
        # TODO: проверить что приходит в result_info...
        files = self._get_published_files()

        for file in files['items']:
            if str(file['path']).endswith(path):
                return file['public_url']

        return ''

    def unpublish(self, path):
        """
        Unpublish folder of file
        :param path: path to file or folder
        """
        url = urljoin(self._base_url, 'resources/unpublish')
        result_info = self.request('put', url, params={'path': path})
        # TODO: проверить result_info

    def files(self):
        """
        :return: List of all files
        """
        url = urljoin(self._base_url, 'resources/files')
        result_info = self.request('get', url)
        files = [File(**item) for item in result_info['items']]
        return files

    def move(self, path_from, path_to):
        """
        Move file or directory
        """
        url = urljoin(self._base_url, 'resources/move')
        payload = {'path': path_to, 'from': path_from}
        self.request('post', url, params=payload)

    def upload(self, path_from, path_to):
        """
        Upload file
        :param path_from: path from
        :param path_to: path to yandex disk
        """
        url = urljoin(self._base_url, 'resources/upload')
        result_info = self.request('get', url, params={'path': path_to})
        upload_link = result_info['href']
        with open(path_from, 'rb') as fh:
            self.request('put', upload_link, files={'file': fh})

    def upload_from_url(self, from_url, path_to):
        """
        Upload file by URL
        :param from_url: URL path from
        :param path_to: path to yandex disk
        """
        url = urljoin(self._base_url, 'resources/upload')
        payload = {'path': path_to, 'url': from_url}
        self.request('post', url, params=payload)

    def _get_published_files(self):
        url = urljoin(self._base_url, 'resources/public')
        result_info = self.request('get', url)
        return result_info
