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
from ctypes import c_ulonglong, pointer, c_wchar_p, windll


def get_free_space_mb(pathname):
    """Return folder/drive free space (in megabytes)."""
    free_bytes = c_ulonglong(0)
    windll.kernel32.GetDiskFreeSpaceExW(c_wchar_p(pathname), None, None, pointer(free_bytes))
    return free_bytes.value / 1024 / 1024
