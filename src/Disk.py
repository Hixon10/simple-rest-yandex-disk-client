#!/usr/bin/python3


class Disk:
    def __init__(self, trash_size, total_space, used_space, system_folders):
        self.trash_size = trash_size
        self.total_space = total_space
        self.used_space = used_space
        self.system_folders = system_folders