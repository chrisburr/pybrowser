import os
from os.path import basename
import stat
from pathlib import PurePosixPath


def is_windows():
    return os.name == 'nt'


def is_hidden(path):
    if is_windows():
        return has_hidden_attribute(path)
    else:
        return basename(path).startswith('.')


def has_hidden_attribute(path):
    return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


def find_child_paths(parent, paths):
    for path in paths:
        rel_path = PurePosixPath(path).relative_to(parent)
        print(parent, rel_path)
        if len(rel_path.parts) == 1:
            yield rel_path
