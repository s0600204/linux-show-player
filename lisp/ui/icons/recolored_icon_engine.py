# Based on "Palette Icon Engine" by Nick 'Kolcha' Korotysh
#
# Source: https://github.com/Kolcha/paletteicon
#
# Original licence:
#   Copyright (C) 2017-2023  Nick Korotysh <nick.korotysh@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


from qtpy.QtCore import (
    QRect,
    QSize,
    Qt,
)
from qtpy.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QIconEngine,
    QPainter,
    QPixmap,
    QPixmapCache,
)
from qtpy.QtSvg import (
    QSvgRenderer,
)


class RecoloredIconEngine(QIconEngine):

    def __init__(self, icon, color, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._brush = QBrush(color)
        self._color = color
        self._icon = icon
        self._renderer = QSvgRenderer()
        self._src_files = {}

    def _render_icon(self,
                     filename: str,
                     size: QSize,
                     brush: QBrush) -> QPixmap:
        output = QPixmap(size)
        output.fill(Qt.transparent)

        painter = QPainter(output)
        self._renderer.load(filename)
        self._renderer.setAspectRatioMode(Qt.KeepAspectRatio)
        self._renderer.render(painter)

        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(output.rect())

        return output

    def paint(self,
              painter: QPainter,
              rect: QRect,
              mode: QIcon.Mode,
              state: QIcon.State):
        size = rect.size() * painter.device().devicePixelRatioF()
        pxm = self.pixmap(size, mode, state)
        pxm.setDevicePixelRatio(painter.device().devicePixelRatioF())
        painter.drawPixmap(rect, pxm)

    def pixmap(self,
               size: QSize,
               *_) -> QPixmap:
        filename = self._icon

        # pylint: disable=consider-using-f-string
        pmckey = "rie_{}:{}x{}:{}".format(
            filename,
            size.width(),
            size.height(),
            self._color.name(QColor.HexArgb))

        pxm = QPixmapCache.find(pmckey)
        if not pxm:
            pxm = self._render_icon(filename, size, self._brush)
            QPixmapCache.insert(pmckey, pxm)
        return pxm
