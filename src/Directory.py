#!/usr/bin/python3

from src.File import File


class Directory():
    def __init__(self, name, created, modified, path, type,
                 mime_type=None, size=None, preview=None, media_type=None, md5=None,
                 public_key=None, _embedded=None, public_url=None):
        self.mime_type = mime_type
        self.preview = preview
        self.size = size
        self.media_type = media_type
        self.md5 = md5
        self.public_key = public_key
        self.public_url = public_url
        self.name = name
        self.created = created
        self.modified = modified
        self.path = path
        self.type = type
        self.children = []

        if _embedded is not None:
            for item in _embedded['items']:
                if item["type"] == "dir":
                    d = Directory(item["name"], item["created"], item["modified"], item["path"], item["type"])
                    self.children.append(d)

                if item["type"] == "file":
                    f = File(**item)
                    self.children.append(f)


    def get_children(self):
        return self.children
