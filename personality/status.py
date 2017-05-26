from .word import *

__all__ = ['Status', 'Statuses']


class Status(object):
    @classmethod
    def __init__(cls, status):
        instance = cls()

        instance.words = list()
        for word in status:
            instance.words.append(Words.__init__(word))

        return instance

class Statuses(object):
    @classmethod
    def __init__(cls, statuses):
        instance = cls()

        instance.statuses = list()

        for status in statuses:
            instance.statuses.append(Status.__init__(status))

        return instance
