# This file is part of Linux Show Player
#
# Copyright 2023 Francesco Ceruti <ceppofrancy@gmail.com>
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

from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit, quote, unquote
import sys


class SessionURI:
    LOCAL_SCHEMES = ("", "file")

    def __init__(self, uri: str = ""):
        split = urlsplit(uri)

        self._is_local = self.is_local_scheme(split.scheme)
        if self._is_local:
            # If the path doesn't start with "/" the first part is interpreted
            # as "netloc", older session have this problem.
            rel_path = split.netloc + split.path
            # We need the absolute path
            path = self.path_to_absolute(rel_path)
            self._uri = urlunsplit(("file", "", path, "", ""))
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

        # On Windows systems, `urlsplit().path` is a string starting with
        # a `/` character, which causes problems. For instance it prevents
        # pathlib from treating as a path that exists.
        path = urlsplit(self._uri).path
        if sys.platform.startswith('win32') and self._is_local:
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
        return self._is_local

    @classmethod
    def path_to_relative(cls, path):
        from lisp.application import Application

        return Application().session.rel_path(path)

    @classmethod
    def path_to_absolute(cls, path):
        from lisp.application import Application

        return Application().session.abs_path(path)

    @classmethod
    def is_local_scheme(cls, scheme):
        return scheme in cls.LOCAL_SCHEMES
