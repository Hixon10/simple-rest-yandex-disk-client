#!/usr/bin/python3
import random
import string
import sys

from src.YandexDiskException import YandexDiskException
from src.YandexDiskRestClient import YandexDiskRestClient


class ExamplesOfUsingOfYandexDiskRestClient:
    def __init__(self):
        token = "ea191c8546be4149a6319d9959328831"
        self.client = YandexDiskRestClient(token)
        self.random_name_of_folder = ExamplesOfUsingOfYandexDiskRestClient.id_generator(10)
        self.random_name_of_child_folder = ExamplesOfUsingOfYandexDiskRestClient.id_generator(10)
        self.random_name_of_child_2_folder = ExamplesOfUsingOfYandexDiskRestClient.id_generator(10)
        self.random_name_of_parent_folder = ExamplesOfUsingOfYandexDiskRestClient.id_generator(10)

    def get_disk_metadata(self):
        try:
            disk = self.client.get_disk_metadata()
            print("total space of disk = " + str(disk.total_space))
            print("used spase of disk = " + str(disk.used_space))
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def creating_of_folder(self):
        folder_name = self.random_name_of_folder

        try:
            self.client.create_folder(folder_name)
            self.client.create_folder(self.random_name_of_parent_folder)
            self.client.create_folder(self.random_name_of_child_folder)
            self.client.create_folder(self.random_name_of_child_2_folder)
            print("Folders was created")
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def get_meta_of_folder(self):
        try:
            directory = self.client.get_content_of_folder(self.random_name_of_folder)
            print("name of a new folder is " + directory.name)
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def remove_folder_or_file(self):
        try:
            self.client.remove_folder_or_file(self.random_name_of_folder)
            print("The folder " + self.random_name_of_folder + " was successfully removed.")
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def copy_folder_of_file(self):
        try:
            self.client.copy_folder_or_file("/" + self.random_name_of_child_folder,
                                            "/" + self.random_name_of_parent_folder + "/" + self.random_name_of_child_folder)
            print(
                "The folder " + self.random_name_of_child_folder + "was copy to folder " + self.random_name_of_parent_folder)
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def move_folder_of_file(self):
        try:
            self.client.move_folder_or_file("/" + self.random_name_of_child_2_folder,
                                            "/" + self.random_name_of_parent_folder + "/" + self.random_name_of_child_2_folder)
            print(
                "The folder " + self.random_name_of_child_2_folder + "was move to folder " + self.random_name_of_parent_folder)
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def get_download_link_to_file(self):
        try:
            link = self.client.get_download_link_to_file("bender.jpg")
            print("Download link to the file bender.jpg is " + link["href"])
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def get_published_files(self):
        try:
            files = self.client.get_published_elements()
            print("There are " + str(len(files)) + " published files.")
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def get_public_link_to_folder_or_file(self):
        try:
            public_link = self.client.get_public_link_to_folder_or_file("bender.jpg")
            print("Public link to the file bender.jpg is " + public_link)
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def unpublish_folder_or_file(self):
        try:
            self.client.unpublish_folder_or_file("bender.jpg")
            print("From this point on, there is no a public link to bender.jpg")
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def get_list_of_all_files(self):
        try:
            files = self.client.get_list_of_all_files()
            print("There are " + str(len(files)) + " files in this Yandex.Disk")
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def upload_file_from_url(self):
        try:
            url = "http://hixon.ru/wp-content/uploads/2014/07/jeett_dt_001.png"
            self.client.upload_file_from_url(url, self.random_name_of_parent_folder + "/jeett_dt_001.png")
            print("File jeett_dt_001.png was downloaded to the folder " + self.random_name_of_parent_folder)
        except YandexDiskException as exp:
            print(exp)
            sys.exit(1)

    def run(self):
        self.get_disk_metadata()
        self.creating_of_folder()
        self.get_meta_of_folder()
        self.remove_folder_or_file()
        self.copy_folder_of_file()
        self.move_folder_of_file()
        self.get_download_link_to_file()
        self.get_published_files()
        self.get_public_link_to_folder_or_file()
        self.unpublish_folder_or_file()
        self.get_list_of_all_files()
        self.upload_file_from_url()

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


def main():
    examples = ExamplesOfUsingOfYandexDiskRestClient()
    examples.run()


if __name__ == "__main__":
    main()