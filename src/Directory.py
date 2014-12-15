#!/usr/bin/python3

from src.File import File


class Directory():
    def __init__(self, _embedded=None, **kwargs):
        self.children = []

        for key in kwargs:
            setattr(self, key, kwargs[key])

        if _embedded is not None:
            for item in _embedded['items']:
                if item["type"] == "dir":
                    d = Directory(**item)
                    self.children.append(d)

                if item["type"] == "file":
                    f = File(**item)
                    self.children.append(f)


    def get_children(self):
        return self.children
