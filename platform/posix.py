# -*- coding: utf-8 -*-
from os import statvfs
from zipimport import zipimporter

# TODO: check for updates to youtube-dl

ydl = zipimporter('youtube-dl').load_module('youtube_dl')
YoutubeDL = ydl.YoutubeDL
list_extractors = ydl.list_extractors

def get_free_space_mb(pathname):
    """Return folder/drive free space (in megabytes)."""
    st = statvfs(pathname)
    return st.f_bavail * st.f_frsize / 1024 / 1024
