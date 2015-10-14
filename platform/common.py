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
from logging import getLogger
from os.path import exists, dirname, join

from git import Repo

log = getLogger(__name__)
repository_url = 'https://github.com/rg3/youtube-dl.git'


def ensure_ydl():
    base_path = dirname(__file__)
    repo_path = join(base_path, 'ydl')

    # Check if it exists
    if not exists(repo_path):
        log.warn('Youtube-dl not found! Dowloading from %s', repository_url)
        Repo.clone_from(repository_url, repo_path)

    # Check if it's old
    else:
        repo = Repo(repo_path)
        remote = repo.remote()
        log.info('Updating from %s', remote.name)
        remote.pull()


ensure_ydl()
from .ydl import youtube_dl

youtube_dl.main('--version')
