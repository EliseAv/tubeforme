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
import re
import tempfile

import requests

from . import _base

log = logging.getLogger(__name__)


class BlogVideoFeed(_base.VideoFeed):
    re_youtube = re.compile(r"\b(v[=/]|embed/|youtu\.be/)([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])", re.MULTILINE)

    def fetch_pages(self):
        for i in self.fetch():
            try:
                log.debug("%s, %s", i.id, i.link)
                log.info("Fetching %s", i.title)
                response = requests.get(i.link)
                html = response.text
                log.debug("Read %d kibibytes." % (len(html) / 1024,))
                yield html
            except Exception:
                log.exception("Failed to fetch %s", i.id, exc_info=True)
            log.debug("")

    def fetch_video_codes(self):
        for html in self.fetch_pages():
            for match in self.re_youtube.finditer(html):
                video = match.group(2)
                log.debug("Found video: %s", video)
                if video == "videoseries":
                    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as file:
                        file.write(html)
                    raise ValueError("URL PARSE ERROR, please check " + file.name)
                yield video
