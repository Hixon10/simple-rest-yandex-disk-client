#!/usr/bin/python3
from src.YandexDiskRestClient import YandexDiskRestClient


def main():
    login = "simple-rest-client"
    password = "fj$*(fhgwuf3wohfe4wwoenfD"
    token = "ea191c8546be4149a6319d9959328831"

    client = YandexDiskRestClient(token)
    client.upload_file_from_url("http://hsto.org/files/da1/3b5/e72/da13b5e7257545f5b70d40881e8ee3a9.jpg", "bender.jpg")


if __name__ == "__main__":
    main()
