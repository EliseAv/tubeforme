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
import ctypes
from logging import getLogger, StreamHandler, DEBUG
from os.path import dirname, join
from platform import system
from os import statvfs

from tendo.singleton import SingleInstance
from yaml import load

from pull import YoutubeChannelVideoFeed, BlogVideoFeed, append_to_queue
from dedup import Deduplicator
from youtube_dl import YoutubeDL

BASEDIR = dirname(__file__)
log = getLogger('tubeforme.main')


def main():
    sentinel = SingleInstance()
    try:
        log.info('Starting. %d MB free.', get_free_space_mb(BASEDIR))
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
    }
    with YoutubeDL(ydl_opts) as ydl:
        for link in open(join(BASEDIR, 'queue.txt')):
            space = get_free_space_mb(BASEDIR)
            if space > 500:
                ydl.download([link])
            else:
                log.fatal("Disk space low, exiting! %d MB free.", space)
                exit(1)


def get_free_space_mb(pathname):
    """Return folder/drive free space (in megabytes)."""
    if system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(pathname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = statvfs(pathname)
        return st.f_bavail * st.f_frsize / 1024 / 1024


if __name__ == '__main__':
    toplog = getLogger('tubeforme')
    toplog.addHandler(StreamHandler())
    toplog.level = DEBUG
    main()
