#!/usr/bin/python3


class YandexDiskException(Exception):
    code = None

    def __init__(self, code, text):
        super(YandexDiskException, self).__init__(text)
        self.code = code

    def __str__(self):
        return "%d. %s" % (self.code, super(YandexDiskException, self).__str__())