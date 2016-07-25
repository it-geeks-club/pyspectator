from collections import MutableMapping, Container
from datetime import datetime, timedelta
from pyvalid import accepts


class LimitedTimeTable(MutableMapping, Container):

    def __init__(self, time_span):
        self.__storage = dict()
        self.__time_span = None
        self.time_span = time_span

    @property
    def time_span(self):
        return self.__time_span

    @time_span.setter
    @accepts(object, timedelta)
    def time_span(self, value):
        self.__time_span = value

    @property
    def oldest(self):
        value = None
        if self.__len__() > 0:
            value = min(self.__storage.keys())
        return value

    @property
    def newest(self):
        value = None
        if self.__len__() > 0:
            value = max(self.__storage.keys())
        return value

    def oldest_keys(self, size):
        for key in self.__get_slice(0, size):
            yield key

    def oldest_values(self, size):
        for key in self.oldest_keys(size):
            yield self.__storage.get(key)

    def oldest_items(self, size):
        for key in self.oldest_keys(size):
            yield (key, self.__storage.get(key))

    def newest_keys(self, size):
        for key in self.__get_slice(-size, None):
            yield key

    def newest_values(self, size):
        for key in self.newest_keys(size):
            yield self.__storage.get(key)

    def newest_items(self, size):
        for key in self.newest_keys(size):
            yield (key, self.__storage.get(key))

    def __get_slice(self, start, end):
        keys = sorted(self.keys())
        return keys[start:end]

    def __getitem__(self, item):
        return self.__storage.__getitem__(item)

    @accepts(object, datetime, object)
    def __setitem__(self, key, value):
        now = datetime.now()
        if key > now:
            raise ValueError('Can\'t set item from future!')
        oldest = self.oldest
        if (oldest is not None) and (oldest != key):
            longest_time_span = now - oldest
            # Item is too old for current timetable
            if longest_time_span >= self.time_span:
                self.__delitem__(oldest)
        return self.__storage.__setitem__(key, value)

    def __delitem__(self, key):
        return self.__storage.__delitem__(key)

    def __len__(self):
        return self.__storage.__len__()

    def __iter__(self):
        return self.__storage.__iter__()

    def __contains__(self, item):
        return self.__storage.__contains__(item)


__all__ = ['LimitedTimeTable']
