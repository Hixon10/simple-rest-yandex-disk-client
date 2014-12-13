#!/usr/bin/python3

from src.Element import Element
from src.File import File


class Directory(Element):
    def __init__(self, name, created, modified, path, typ):
        super().__init__(name, created, modified, path, typ)
        self.children = []

    @staticmethod
    def get_instance(dictionary_params):
        directory = Directory(dictionary_params["name"], dictionary_params["created"], dictionary_params["modified"],
                              dictionary_params["path"], dictionary_params["type"])


        if "_embedded" in dictionary_params:
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