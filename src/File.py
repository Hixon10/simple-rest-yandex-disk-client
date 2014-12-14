#!/usr/bin/python3

class File():
    def __init__(self, name, created, modified, media_type, path, md5, type, mime_type, size,
                 public_key=None, public_url=None, preview=None):
        self.public_url = public_url
        self.preview = preview
        self.name = name
        self.created = created
        self.modified = modified
        self.path = path
        self.type = type
        self.media_type = media_type
        self.md5 = md5
        self.mime_type = mime_type
        self.size = size