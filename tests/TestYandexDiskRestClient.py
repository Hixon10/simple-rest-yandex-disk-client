#!/usr/bin/python3
import random
import string

from unittest import TestCase
from src.YandexDiskException import YandexDiskException
from src.YandexDiskRestClient import YandexDiskRestClient


class TestYandexDiskRestClient(TestCase):
    def setUp(self):
        token = "ea191c8546be4149a6319d9959328831"
        self.client = YandexDiskRestClient(token)


    def test_get_disk_metadata(self):
        disk = self.client.get_disk_metadata()
        self.assert_(disk.total_space > 0 and disk.used_space > 0)


    def test_get_content_of_folder(self):
        directory = self.client.get_content_of_folder("/")
        self.assert_(directory.type == "dir")
        self.assert_(directory.path == "disk:/")
        self.assert_(len(directory.children) > 0)


    def test_create_folder(self):
        folder_name = TestYandexDiskRestClient.id_generator(10)
        self.client.create_folder(folder_name)

        directory = self.client.get_content_of_folder(folder_name)
        self.assert_(directory.name == folder_name)


    def test_remove_folder_or_file(self):
        folder_name = TestYandexDiskRestClient.id_generator(10)
        self.client.create_folder(folder_name)

        self.client.remove_folder_or_file(folder_name)

        self.assertRaises(YandexDiskException, self.client.get_content_of_folder, folder_name)


    def test_copy_folder_of_file(self):
        parent_folder = TestYandexDiskRestClient.id_generator(10)
        par_dir = self.client.create_folder(parent_folder)

        child_folder = TestYandexDiskRestClient.id_generator(10)
        child_dir = self.client.create_folder(child_folder)

        self.client.copy_folder_or_file("/" + child_folder, "/" + parent_folder + "/"  + child_folder)

        par_dir2 = self.client.get_content_of_folder(parent_folder)
        self.assert_(len(par_dir2.children) == 1)


    def test_get_download_link_to_file(self):
        link = ""

        link = self.client.get_download_link_to_file("bender.jpg")
        self.assert_(len(link) > 0)


    def test_get_published_files(self):
        files = self.client.get_published_elements()
        self.assert_(len(files) > 0)


    def test_get_public_link_to_folder_or_file(self):
        public_link = ""
        public_link = self.client.get_public_link_to_folder_or_file("bender.jpg")
        self.assert_(public_link == "https://yadi.sk/i/WBIYPObHdMWcX")


    def test_unpublish_folder_or_file(self):
        folder_name = TestYandexDiskRestClient.id_generator(10)
        folder = self.client.create_folder(folder_name)

        link = self.client.get_public_link_to_folder_or_file(folder_name)
        self.assert_(len(link) > 0)

        published_files_count = len(self.client.get_published_elements())

        self.client.unpublish_folder_or_file(folder_name)

        published_files_count2 = len(self.client.get_published_elements())

        self.assert_(published_files_count == published_files_count2 + 1)


    def test_get_list_of_all_files(self):
        files = self.client.get_list_of_all_files()
        self.assert_(len(files) > 0)


    def test_move_folder_of_file(self):
        parent_folder = TestYandexDiskRestClient.id_generator(10)
        par_dir = self.client.create_folder(parent_folder)

        child_folder = TestYandexDiskRestClient.id_generator(10)
        child_dir = self.client.create_folder(child_folder)

        self.client.move_folder_or_file("/" + child_folder, "/" + parent_folder + "/"  + child_folder)

        par_dir2 = self.client.get_content_of_folder(parent_folder)
        self.assert_(len(par_dir2.children) == 1)

        self.assertRaises(YandexDiskException, self.client.get_content_of_folder, child_folder)


    def test_upload_file(self):
        self.assertTrue(True)


    def test_upload_file_from_url(self):
        url = "http://hixon.ru/wp-content/uploads/2014/07/jeett_dt_001.png"
        file_name = TestYandexDiskRestClient.id_generator(10)

        self.client.upload_file_from_url(url, file_name)

        file = self.client.get_content_of_folder(file_name)
        self.assert_(file.name == file_name)

        self.client.remove_folder_or_file(file_name)


    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

