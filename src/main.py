#!/usr/bin/python3

import requests


class Disk:
    def __init__(self, trash_size, total_space, used_space, system_folders):
        self.trash_size = trash_size
        self.total_space = total_space
        self.used_space = used_space
        self.system_folders = system_folders


class Element:
    def __init__(self, name, created, modified, path, typ):
        self.name = name
        self.created = created
        self.modified = modified
        self.path = path
        self.type = typ

    def is_dir(self):
        return False

    def is_file(self):
        return False


class File(Element):
    def __init__(self, name, created, modified, media_type, path, md5, typ, mime_type, size):
        super().__init__(name, created, modified, path, typ)
        self.media_type = media_type
        self.md5 = md5
        self.mime_type = mime_type
        self.size = size

    @staticmethod
    def get_instance(dictionary_params):
        f = File(dictionary_params["name"], dictionary_params["created"], dictionary_params["modified"], dictionary_params["media_type"], dictionary_params["path"], dictionary_params["md5"], dictionary_params["type"], dictionary_params["mime_type"], dictionary_params["size"])
        return f

    def is_dir(self):
        return False

    def is_file(self):
        return True


class Directory(Element):
    def __init__(self, name, created, modified, path, typ):
        super().__init__(name, created, modified, path, typ)
        self.children = []

    @staticmethod
    def get_instance(dictionary_params):
        directory = Directory(dictionary_params["name"], dictionary_params["created"], dictionary_params["modified"],
                              dictionary_params["path"], dictionary_params["type"])

        for item in dictionary_params["_embedded"]["items"]:
            if item["type"] == "dir":
                d = Directory(item["name"], item["created"], item["modified"], item["path"], item["type"])
                directory.children.append(d)

            if item["type"] == "file":
                f = File.get_instance(item)
                directory.children.append(f)

        return directory

    def get_children(self):
        return self.children

    def is_dir(self):
        return True

    def is_file(self):
        return False


class YandexDiskException(Exception):
    code = None

    def __init__(self, code, text):
        super(YandexDiskException, self).__init__(text)
        self.code = code

    def __str__(self):
        return "%d. %s" % (self.code, super(YandexDiskException, self).__str__())


class YandexDiskRestClient:
    _base_url = "https://cloud-api.yandex.net:443/v1/disk"

    def __init__(self, login, password, token):
        self.login = login
        self.password = password
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
        url = self._base_url + "/resources/public"

        r = requests.get(url, headers=self.base_headers)
        self._check_code(r)

        json_dict = r.json()

        files = []

        for item in json_dict["items"]:
            f = File.get_instance(item)
            files.append(f)

        return files

    def get_public_link_to_folder_or_file(self, path):
        url = self._base_url + "/resources/publish"

        payload = {'path': path}
        r = requests.get(url, headers=self.base_headers, params=payload)
        self._check_code(r)

        json_dict = r.json()
        return json_dict["href"]

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

    def _check_code(self, req):
        if not str(req.status_code).startswith("2"):
            raise YandexDiskException(req.status_code, req.text)


def main():
    login = "simple-rest-client"
    password = "fj$*(fhgwuf3wohfe4wwoenfD"
    token = "ea191c8546be4149a6319d9959328831"

    client = YandexDiskRestClient(login, password, token)
    client.get_published_files()


if __name__ == "__main__":
    main()
