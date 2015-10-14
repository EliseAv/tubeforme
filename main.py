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
from os import getcwd, mkdir
from os.path import join, exists
from sys import argv

from tendo.singleton import SingleInstance
from yaml import load

from .dedup import Deduplicator
from .pull import YoutubeChannelVideoFeed, BlogVideoFeed
from .platform import YoutubeDL, get_free_space_mb

BASEDIR = getcwd()
log = getLogger('tubeforme.main')


def main():
    sentinel = SingleInstance()
    try:
        log.info('Starting. %d MB free.', get_free_space_mb(BASEDIR))
        if 'skip' not in argv:
            try:
                find_new_stuff()
            except FileNotFoundError:
                pass

        try:
            deduplicate()
        except FileNotFoundError:
            pass

        try:
            download_found_stuff()
        except FileNotFoundError:
            pass
    finally:
        del sentinel


def find_new_stuff():
    queue_path = join(BASEDIR, 'queue.txt')
    known_path = join(BASEDIR, 'known.json')
    settings = load(open(join(BASEDIR, 'subscriptions.yaml'), 'r'))
    for channel in settings['youtube_channels']:
        YoutubeChannelVideoFeed(known_path, channel).append_to_queue(queue_path)
    for blog in settings['blogs']:
        BlogVideoFeed(known_path, blog).append_to_queue(queue_path)


def deduplicate():
    ded = Deduplicator(BASEDIR, 'videos', 'queue.txt')
    ded.main()


def download_found_stuff():
    download_path = join(BASEDIR, 'videos')
    if not exists(download_path):
        mkdir(download_path)
    ydl_opts = {
        'writedescription': True,
        'noprogress': True,
        # 'writesubtitles': True,
        'outtmpl': join(download_path, '%(title)s %(uploader)s-%(id)s.%(ext)s'),
    }
    with YoutubeDL(ydl_opts) as ydl:
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
