#!/usr/bin/python3

import requests


class YandexDiskRestClient:
    _base_url = "https://cloud-api.yandex.net:443/v1/disk"

    def __init__(self, login, password, token):
        self.login = login
        self.password = password
        self.token = token

        self.base_headers = {
            "Accept"        :   "application/json",
            "Authorization" :   "OAuth " + self.token,
            "User-Agent"    :   "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Host"          :   "cloud-api.yandex.net"
        }

    def get_base_url(self):
        return YandexDiskRestClient._base_url

    def get_file_metadata(self):
        url = self._base_url + ""

        r = requests.get(url, headers=self.base_headers)
        print(r.text)


def main():
    login = "simple-rest-client"
    password = "fj$*(fhgwuf3wohfe4wwoenfD"
    token = "ea191c8546be4149a6319d9959328831"

    client = YandexDiskRestClient(login, password, token)
    client.get_file_metadata()


if __name__ == "__main__":
    main()
