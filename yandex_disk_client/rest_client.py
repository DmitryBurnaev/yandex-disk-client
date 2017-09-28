from urllib.parse import urljoin

import requests
from requests import request

from .core import Directory, Disk, File
from .exceptions import YandexDiskException

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
        response = request(method, url, **kwargs)
        self._check_code(response)
        response_data = response.json()
        return response_data

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
        json_dict = self._get_dictionary_of_published_files()

        elements = []

        for item in json_dict["items"]:
            if item["type"] == "dir":
                elements.append(Directory(**item))
            elif item["type"] == "file":
                elements.append(File(**item))

        return elements

    def get_public_link_to_folder_or_file(self, path):
        """
        :param path: path
        :return: public link to folder or file
        """
        url = self._base_url + "/resources/publish"

        payload = {'path': path}
        r = requests.put(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        files = self._get_dictionary_of_published_files()

        for file in files["items"]:
            if str(file["path"]).endswith(path):
                return file["public_url"]

        return ""

    def unpublish_folder_or_file(self, path):
        """
        Unpublish folder of file
        :param path: path to file or folder
        """
        url = self._base_url + "/resources/unpublish"

        payload = {'path': path}
        r = requests.put(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def get_list_of_all_files(self):
        """
        :return: List of all files
        """
        url = self._base_url + "/resources/files"

        r = requests.get(url, headers=self.base_headers)
        self._check_code(r)

        json_dict = r.json()

        files = []

        for item in json_dict["items"]:
            f = File(**item)
            files.append(f)

        return files

    def move_folder_or_file(self, path_from, path_to):
        """
        Move folder or file
        :param path_from: path from
        :param path_to: path to
        """
        url = self._base_url + "/resources/move"

        payload = {'path': path_to, 'from': path_from}
        r = requests.post(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def upload_file(self, path_from, path_to):
        """
        Upload file
        :param path_from: path from
        :param path_to: path to yandex disk
        """
        url = self._base_url + "/resources/upload"

        payload = {'path': path_to}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        upload_link = json_dict["href"]

        with open(path_from, 'rb') as fh:
            files = {'file': fh}

            r2 = requests.put(upload_link, headers=self.base_headers, files=files)
            self._check_code(r2)

    def upload_file_from_url(self, from_url, path_to):
        """
        Upload file by URL
        :param from_url: URL path from
        :param path_to: path to yandex disk
        """
        url = self._base_url + "/resources/upload"

        payload = {'path': path_to, 'url': from_url}
        r = requests.post(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def _get_dictionary_of_published_files(self):
        url = self._base_url + "/resources/public"

        r = requests.get(url, headers=self.base_headers)
        self._check_code(r)

        return r.json()

    def _check_code(self, req):
        if not str(req.status_code).startswith("2"):
            raise YandexDiskException(req.status_code, req.text)


