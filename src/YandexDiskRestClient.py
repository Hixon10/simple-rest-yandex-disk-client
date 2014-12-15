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
            "Host": "cloud-api.yandex.net"
        }

    def get_disk_metadata(self):
        """
        Получить метаинформацию о диске пользователя
        :return: метаинформация о диске
        """
        url = self._base_url

        r = requests.get(url, headers=self.base_headers)
        self._check_code(r)

        json_dict = r.json()

        disk = Disk(json_dict["trash_size"], json_dict["total_space"], json_dict["used_space"],
                    json_dict["system_folders"])
        return disk

    def get_content_of_folder(self, path_to_folder):
        """
        Получить содержимое папки
        :param path_to_folder: путь до папки
        :return: содержимое папки
        """
        url = self._base_url + "/resources"

        payload = {'path': path_to_folder}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        d = Directory(**json_dict)
        return d

    def create_folder(self, path_to_folder):
        """
        Создать папку
        :param path_to_folder: путь до папки
        :return: созданная папка
        """
        url = self._base_url + "/resources"

        payload = {'path': path_to_folder}
        r = requests.put(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        d = self.get_content_of_folder(path_to_folder)
        return d

    def remove_folder_or_file(self, path):
        """
        Удалить папку или файл
        :param path: путь до ресурса
        """
        url = self._base_url + "/resources"

        payload = {'path': path}
        r = requests.delete(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def copy_folder_of_file(self, path_from, path_to):
        """
        Копировать файл или папку
        :param path_from: путь ОТ
        :param path_to: путь КУДА
        """
        url = self._base_url + "/resources/copy"

        payload = {'path': path_to, 'from': path_from}
        r = requests.post(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def get_download_link_to_file(self, path_to_file):
        """
        Получить ссылку на скачивание файла
        :param path_to_file: путь до файла
        :return: ссылка на файл
        """
        url = self._base_url + "/resources/download"

        payload = {'path': path_to_file}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        return json_dict["href"]

    def get_published_elements(self):
        """
        Получить список публичных элементов диска
        :return: список публичных элементов диска
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
        Получить публичную ссылку на файл или папку
        :param path: путь до файла или папки
        :return: публичная ссылка на файл или папку
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
        Сделать файл или папку приватными
        :param path: путь до файла или папки
        """
        url = self._base_url + "/resources/unpublish"

        payload = {'path': path}
        r = requests.put(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def get_list_of_all_files(self):
        """
        Получить список всех файлов на диске
        :return: список всех файлов на диске
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

    def move_folder_of_file(self, path_from, path_to):
        """
        Переместить файл или папку
        :param path_from: путь ОТ
        :param path_to: путь ДО
        """
        url = self._base_url + "/resources/move"

        payload = {'path': path_to, 'from': path_from}
        r = requests.post(url, headers=self.base_headers, params=payload)
        self._check_code(r)

    def upload_file(self, path_from, path_to):
        """
        Загрузить файл
        :param path_from: физический путь до файла
        :param path_to: путь на яндекс диске
        """
        url = self._base_url + "/resources/upload"

        payload = {'path': path_to}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        upload_link = json_dict["href"]

        uploaded_file = open(path_from, 'rb')
        files = {'file': uploaded_file}

        r2 = requests.put(upload_link, headers=self.base_headers, files=files)

        uploaded_file.close()

        self._check_code(r2)

    def upload_file_from_url(self, from_url, path_to):
        """
        Загрузить файл по URL
        :param from_url: путь до файла URL
        :param path_to: путь на яндекс диске
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


