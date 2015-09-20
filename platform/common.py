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
from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta
from logging import getLogger
from os.path import getmtime, exists, basename
from subprocess import call
from zipimport import zipimporter

from wget import download

log = getLogger(__name__)


def load_ydl(command):
    # Check if it exists
    if not exists(command):
        url = 'https://yt-dl.org/downloads/latest/' + basename(command)
        log.error('%s not found! Downloading from: %s', command, url)
        download(url, command)

    # Check if it's old
    if datetime.now() - datetime.fromtimestamp(getmtime(command)) > timedelta(days=1):
        log.info('%s is old. Updating.', command)
        call([command, '-U'])
        with open(command, 'ab'):
            # just touch the file to update its mtime in case it did not update
            pass

    # Load it and expose it.
    ydl = zipimporter(command).load_module('youtube_dl')
    log.debug('youtube-dl loaded.')
    return ydl.YoutubeDL, ydl.list_extractors
