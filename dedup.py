# -*- coding: utf-8 -*-
#
# Copyright 2008-2019, Ekevoo.com.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
from collections import defaultdict
from logging import getLogger
from os import listdir, rename, unlink
from os.path import exists, join, splitext
from re import compile

from .platform import list_extractors

log = getLogger(__name__)


class Deduplicator:
    def __init__(self, base, inv, queue):
        self._queuepath = join(base, queue)
        self._invpath = join(base, inv)

    ids_in_filenames = {"youtube": compile(r"-([a-zA-Z0-9_-]{11})$")}

    extractors = list(reversed(list_extractors(None)))  # Reversed to keep YouTube close to the top.

    @classmethod
    def url_service_and_code(cls, url):
        for ie in cls.extractors:
            if ie.working() and ie.suitable(url) and hasattr(ie, "extract_id"):
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
            if extension.lower() not in (".description", ".part"):
                service, code = self.filename_service_and_code(name)
                if service and code:
                    result[service].add(code)
        return result

    def main(self, pretend=False):
        inventory = self.get_obtained_files()
        keep_those = []
        discarded_count = 0
        log.debug("Currently with %d files.", sum([len(s) for s in inventory.values()]))
        for url in open(self._queuepath, "r"):
            if not url.strip():
                continue  # Blank line, skip!
            service, code = self.url_service_and_code(url.strip())
            if service and code and code in inventory[service]:
                discarded_count += 1
            else:
                keep_those.append(url)
                inventory[service].add(code)  # Discard future duplicates.
        if pretend:
            log.debug("Discarded %d items. These stayed:", discarded_count)
            for i in keep_those:
                log.debug(i.strip())
        elif discarded_count > 0:
            backup = self._queuepath + "~"
            if exists(backup):
                unlink(backup)
            rename(self._queuepath, backup)
            with open(self._queuepath, "w") as f:
                f.writelines(keep_those)
