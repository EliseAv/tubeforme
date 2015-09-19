# -*- coding: utf-8 -*-
from zipimport import zipimporter
import ctypes

# TODO: check if we are running python 2 and not python 3. the youtube-dl.exe is py2 only.
# TODO: check for updates to youtube-dl

ydl = zipimporter('youtube-dl.exe').load_module('youtube_dl')
YoutubeDL = ydl.YoutubeDL
list_extractors = ydl.list_extractors


def get_free_space_mb(pathname):
    """Return folder/drive free space (in megabytes)."""
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(pathname), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value / 1024 / 1024
