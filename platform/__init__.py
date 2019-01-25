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
from logging import getLogger
from os import name

from .common import ensure_ydl

if name == 'nt':  # Windows
    from .nt import get_free_space_mb
elif name == 'posix':  # Linux and OSX
    from .posix import get_free_space_mb
else:
    getLogger(__name__).fatal('Unknown os! %s', name)
    exit(1)

ensure_ydl()
from .ydl.youtube_dl import main, YoutubeDL, gen_extractors, list_extractors
