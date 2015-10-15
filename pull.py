# -*- coding: utf-8 -*-
#
# Copyright 2008-2015, Ekevoo.com.
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
from json import dump, load
from logging import getLogger
from re import compile, MULTILINE
from urllib.request import urlopen

from feedparser import parse

log = getLogger(__name__)


class VideoFeed:
    def __init__(self, known_path, url):
        self.url = url
        self.read_list = ReadList(known_path, url)

    def is_new(self, item):
        return self.read_list.is_new(item.id)

    def fetch(self):
        try:
            feed = parse(self.url)
            items = feed.entries
            if len(items) == 0:
                raise Exception('Empty feed. Is site down?')
            new_items = list(filter(self.is_new, items))
            print('Feed contains %d items, %d are new.' % (len(items), len(new_items)))
            # iterate first, then save new read list
            for i in new_items:
                yield i
            self.read_list.save()
        except:
            print('Unexpected error with', self.url)
            print(sys.exc_info()[0])

    def fetch_video_codes(self):
        raise NotImplementedError

    def append_to_queue(self, queue_path):
        codes = self.fetch_video_codes()
        links = ['\nhttp://www.youtube.com/watch?v=' + v for v in codes]
        f = open(queue_path, 'a')
        f.writelines(links)
        f.close()


class BlogVideoFeed(VideoFeed):
    re_youtube = compile('\\b(v[=/]|embed/|youtu\.be/)([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])', MULTILINE)

    def fetch_pages(self):
        for i in self.fetch():
            try:
                print(i.id, i.link)
                print('Fetching ' + i.title)
                response = urlopen(i.link)
                html = response.read().decode(errors='replace')
                print('Read %d kibibytes.' % (len(html) / 1024,))
                yield html
            except:
                print('Unexpected error:', sys.exc_info())
            print()

    def fetch_video_codes(self):
        for html in self.fetch_pages():
            for match in self.re_youtube.finditer(html):
                video = match.group(2)
                print('Found video:', video)
                yield video


class YoutubeChannelVideoFeed(VideoFeed):
    def __init__(self, known_path, channel):
        VideoFeed.__init__(self, known_path, 'https://www.youtube.com/feeds/videos.xml?channel_id=' + channel)

    def fetch_video_codes(self):
        for item in self.fetch():
            video = item.id[-11:]  # sometimes it can be this easy :)
            print('Found video: http://youtu.be/' + video)
            yield video


class ReadList:  # this class is not thread-safe at all!
    lists = None

    def __init__(self, filename, key):
        # static initialization
        if ReadList.lists is None:
            try:
                f = open(filename)
                ReadList.lists = load(f)
                f.close()
            except:
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
        f = open(self.filename, 'w')
        dump(ReadList.lists, f, indent=4, sort_keys=True)
        f.close()
