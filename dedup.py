#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from logging import getLogger
from os import listdir, replace
from os.path import splitext, join, dirname
from re import compile

from youtube_dl import list_extractors

log = getLogger('dedup')


class Deduplicator:
    def __init__(self, base, queue, inv):
        self._queuepath = join(base, queue)
        self._invpath = join(base, inv)

    ids_in_filenames = {
        'youtube': compile(r'-([a-zA-Z0-9_-]{11})$'),
    }

    @staticmethod
    def url_service_and_code(url):
        for ie in list_extractors(None):
            if ie.working() and ie.suitable(url):
                return ie.IE_NAME, ie.extract_id(url)
        return None, None

    @classmethod
    def filename_service_and_code(cls, name):
        for service, regex in cls.ids_in_filenames.items():
            match = regex.search(name)
            if match:
                return service, match.group(1)
        return None, None

    def get_obtained_files(self):
        result = defaultdict(set)
        for filename in listdir(self._invpath):
            name, extension = splitext(filename)
            if extension.lower() not in ('.description', '.part'):
                service, code = self.filename_service_and_code(name)
                if service and code:
                    result[service].add(code)
        return result

    def main(self):
        inventory = self.get_obtained_files()
        keep_those = []
        discarded_count = 0
        log('Currently with %d files.', sum([len(s) for s in inventory.values()]))
        for url in open(self._queuepath, 'r'):
            service, code = self.url_service_and_code(url.strip())
            if service and code and code in inventory[service]:
                discarded_count += 1
            else:
                keep_those.append(url)
                inventory[service].add(code)  # Discard future duplicates.
        if discarded_count > 0:
            backup = self._queuepath + '~'
            replace(self._queuepath, backup)
            with open(self._queuepath, 'w') as f:
                f.writelines(keep_those)


if __name__ == '__main__':
    ded = Deduplicator(dirname(__file__), 'videos', 'queue.txt')
    ded.main()
