#!/usr/bin/python3

from src.File import File


class Directory():
    def __init__(self, _embedded=None, *initial_data, **kwargs):
        self.children = []

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
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
