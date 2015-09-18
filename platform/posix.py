# -*- coding: utf-8 -*-
from os import statvfs


def get_free_space_mb(pathname):
    """Return folder/drive free space (in megabytes)."""
    st = statvfs(pathname)
    return st.f_bavail * st.f_frsize / 1024 / 1024
