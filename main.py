#!/usr/bin/env python3
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
from logging import getLogger, StreamHandler, DEBUG
from os.path import dirname, join
from os import statvfs
from platform import system
from sys import argv
from zipimport import zipimporter

from tendo.singleton import SingleInstance
from yaml import load

from .pull import YoutubeChannelVideoFeed, BlogVideoFeed, append_to_queue
from .dedup import Deduplicator

BASEDIR = dirname(__file__)
log = getLogger('tubeforme.main')


def main():
    sentinel = SingleInstance()
    try:
        log.info('Starting. %d MB free.', get_free_space_mb(BASEDIR))
        if 'skip' not in argv:
            find_new_stuff()
        deduplicate()
        dowload_found_stuff()
    finally:
        del sentinel


def find_new_stuff():
    subscriptions = open('subscriptions.yaml', 'r')
    settings = load(subscriptions)
    for channel in settings['youtube_channels']:
        append_to_queue(YoutubeChannelVideoFeed(channel))
    for blog in settings['blogs']:
        append_to_queue(BlogVideoFeed(blog))


def deduplicate():
    ded = Deduplicator(BASEDIR, 'videos', 'queue.txt')
    ded.main()


def dowload_found_stuff():
    ydl_opts = {
        'writedescription': True,
        'noprogress': True,
        'writesubtitles': True,
        'output': join(BASEDIR, 'videos', '%(title)s %(uploader)s-%(id)s.%(ext)s'),
    }
    ydl = zipimporter('youtube-dl').load_module('youtube_dl')
    with ydl.YoutubeDL(ydl_opts) as ydl:
        for link in open(join(BASEDIR, 'queue.txt')):
            space = get_free_space_mb(BASEDIR)
            link = link.strip()
            if link and space > 500:
                ydl.download([link])
            else:
                log.fatal("Disk space low, exiting! %d MB free.", space)
                exit(1)



if __name__ == '__main__':
    toplog = getLogger('tubeforme')
    toplog.addHandler(StreamHandler())
    toplog.level = DEBUG
    main()
