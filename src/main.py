#!/usr/bin/python3

import requests

from src.Directory import Directory
from src.Disk import Disk
from src.File import File
from src.YandexDiskException import YandexDiskException


class YandexDiskRestClient:
    _base_url = "https://cloud-api.yandex.net:443/v1/disk"

    def __init__(self, token):
        self.token = token

        self.base_headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + self.token,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Host": "cloud-api.yandex.net"
        }

    def get_disk_metadata(self):
        url = self._base_url + ""

        r = requests.get(url, headers=self.base_headers)
        self._check_code(r)

        json_dict = r.json()

        disk = Disk(json_dict["trash_size"], json_dict["total_space"], json_dict["used_space"],
                    json_dict["system_folders"])
        return disk

    def get_content_of_folder(self, path_to_folder):
        url = self._base_url + "/resources"

        payload = {'path': path_to_folder}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        d = Directory.get_instance(json_dict)
        return d

    def create_folder(self, path_to_folder):
        url = self._base_url + "/resources"

        payload = {'path': path_to_folder}
        r = requests.put(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        d = self.get_content_of_folder(path_to_folder)
        return d

    def remove_folder_or_file(self, path):
        url = self._base_url + "/resources"

        payload = {'path': path}
        r = requests.delete(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def copy_folder_of_file(self, path_from, path_to):
        url = self._base_url + "/resources/copy"

        payload = {'path': path_to, 'from': path_from}
        r = requests.post(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def get_download_link_to_file(self, path_to_file):
        url = self._base_url + "/resources/download"

        payload = {'path': path_to_file}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        return json_dict["href"]

    def get_published_files(self):
        json_dict = self._get_dictionary_of_published_files()

        files = []

        for item in json_dict["items"]:
            f = File.get_instance(item)
            files.append(f)

        return files

    def get_public_link_to_folder_or_file(self, path):
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
        url = self._base_url + "/resources/unpublish"

        payload = {'path': path}
        r = requests.put(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def get_list_of_all_files(self):
        url = self._base_url + "/resources/files"

        r = requests.get(url, headers=self.base_headers)
        self._check_code(r)

        json_dict = r.json()

        files = []

        for item in json_dict["items"]:
            f = File.get_instance(item)
            files.append(f)

        return files

    def move_folder_of_file(self, path_from, path_to):
        url = self._base_url + "/resources/move"

        payload = {'path': path_to, 'from': path_from}
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


def main():
    login = "simple-rest-client"
    password = "fj$*(fhgwuf3wohfe4wwoenfD"
    token = "ea191c8546be4149a6319d9959328831"

    client = YandexDiskRestClient(token)
    client.unpublish_folder_or_file("Горы.jpg")


if __name__ == "__main__":
    main()
