#!/usr/bin/python3

class Element:
    def __init__(self, name, created, modified, path, typ):
        self.name = name
        self.created = created
        self.modified = modified
        self.path = path
        self.type = typ

    def is_dir(self):
        return False

    def is_file(self):
        return False