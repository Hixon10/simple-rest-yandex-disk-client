#!/usr/bin/python3

from src.Element import Element


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