#!/usr/bin/python3

from src.File import File


class Directory():
    def __init__(self, **kwargs):
        self.children = []

        for key in kwargs:
            if key is not "_embedded":
                setattr(self, key, kwargs[key])

        if "_embedded" in kwargs:
            for item in kwargs["_embedded"]['items']:
                if item["type"] == "dir":
                    d = Directory(**item)
                    self.children.append(d)

                if item["type"] == "file":
                    f = File(**item)
                    self.children.append(f)


    def get_children(self):
        return self.children
