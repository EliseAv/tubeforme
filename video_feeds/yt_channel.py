# -*- coding: utf-8 -*-
#
# Copyright 2008-2017, Ekevoo.com.
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

from . import _base

log = logging.getLogger(__name__)


class YoutubeChannelVideoFeed(_base.VideoFeed):
    def __init__(self, known_path, channel):
        super().__init__(known_path, "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel)

    def fetch_video_codes(self):
        for item in self.fetch():
            video = item.id[-11:]  # sometimes it can be this easy :)
            log.info("Found video: https://youtu.be/%s", video)
            yield video
