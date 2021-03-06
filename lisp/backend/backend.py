# This file is part of Linux Show Player
#
# Copyright 2016 Francesco Ceruti <ceppofrancy@gmail.com>
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

from abc import abstractmethod, ABCMeta

from lisp.core.session_uri import SessionURI
from .media import Media
from .waveform import Waveform


class Backend(metaclass=ABCMeta):
    """Common interface that any backend must provide.

    An __init__() method can be defined if the backend require initialization.
    """

    @abstractmethod
    def uri_duration(self, uri: SessionURI) -> int:
        """Return the file duration in milliseconds.

        :param uri: The URI of the file
        """

    @abstractmethod
    def uri_tags(self, uri: SessionURI) -> dict:
        """Return a dictionary containing the file metadata/tags.

        :param uri: The URI of the file
        """

    @abstractmethod
    def supported_extensions(self) -> dict:
        """Return file extensions supported by the backend.

        Extensions will be categorized in 'audio' and 'video', optionally the
        backend can create others categories.
        e.g. {'audio': ['wav', 'mp3', ...], 'video': ['mp4', 'mov', ...]}
        """

    def media_waveform(self, media: Media) -> Waveform:
        """Return a Waveform object capable of loading the waveform of the given media."""
        return self.uri_waveform(media.input_uri(), media.duration)

    @abstractmethod
    def uri_waveform(self, uri: SessionURI, duration=None) -> Waveform:
        """Return a Waveform object capable of loading the waveform of the given uri."""
