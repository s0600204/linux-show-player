# This file is part of Linux Show Player
#
# Copyright 2024 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

import sys
from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit, quote, unquote


class SessionURI:
    def __init__(self, uri: str = ""):
        split = urlsplit(uri)

        if split.scheme == "" or len(split.scheme) == 1:
            self._uri = urlunsplit(("file", "", quote(self.path_to_absolute(uri)), "", ""))
        else:
            self._uri = uri

    @property
    def relative_path(self):
        """The path relative to the session file. Make sense for local files."""
        return self.path_to_relative(self.absolute_path)

    @property
    @lru_cache(maxsize=256)
    def absolute_path(self):
        """Unquoted "path" component of the URI."""
        path = urlsplit(self._uri).path

        # On Windows systems, `urlsplit().path` is a string starting with
        # a `/` character, which causes problems. For instance, it prevents
        # pathlib from treating it as a path that exists.
        if sys.platform.startswith("win32") and path[0] == "/":
            path = path[1:]

        # We can cache this, the absolute path doesn't change
        return unquote(path)

    @property
    def uri(self):
        """The raw URI string."""
        return self._uri

    @property
    def unquoted_uri(self):
        """The URI string, unquoted."""
        return unquote(self._uri)

    @property
    def is_local(self):
        """True if the URI point to a local file."""
        return urlsplit(self._uri).scheme == "file"

    @classmethod
    def path_to_relative(cls, path):
        from lisp.application import Application

        return Application().session.rel_path(path)

    @classmethod
    def path_to_absolute(cls, path):
        from lisp.application import Application

        return Application().session.abs_path(path)
