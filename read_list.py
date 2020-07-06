# -*- coding: utf-8 -*-
#
# Copyright 2011-2020, Ekevoo.com.
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
import json


class ReadList:  # this class is not thread-safe at all!
    lists = None

    def __init__(self, filename, key):
        # static initialization
        if ReadList.lists is None:
            try:
                f = open(filename)
                ReadList.lists = json.load(f)
                f.close()
            except Exception:
                ReadList.lists = {}
        # instance initialization
        self.key = key
        self.known = ReadList.lists.get(key, [])
        self.new = []
        self.filename = filename

    def is_new(self, item):
        self.new.append(item)
        return item not in self.known

    def save(self):
        ReadList.lists[self.key] = self.known = self.new
        self.new = []
        f = open(self.filename, "w")
        json.dump(ReadList.lists, f, indent=4, sort_keys=True)
        f.close()
