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
import logging

import feedparser
import requests

from .. import read_list

log = logging.getLogger(__name__)


class VideoFeed:
    def __init__(self, known_path, url):
        self.url = url
        self.read_list = read_list.ReadList(known_path, url)

    def is_new(self, item):
        return self.read_list.is_new(item.id)

    def fetch(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            items = feed.entries
            if len(items) == 0:
                raise Exception("Empty feed. Is site down?")
            new_items = list(filter(self.is_new, items))
            log.info("Feed contains %d items, %d are new." % (len(items), len(new_items)))
            # iterate first, then save new read list
            for i in new_items:
                yield i
            self.read_list.save()
        except Exception:
            log.exception("Unexpected error with %s", self.url, exc_info=True)

    def fetch_video_codes(self):
        raise NotImplementedError

    def append_to_queue(self, queue_path):
        codes = self.fetch_video_codes()
        links = ["\nhttps://www.youtube.com/watch?v=" + v for v in codes]
        f = open(queue_path, "a")
        f.writelines(links)
        f.close()
