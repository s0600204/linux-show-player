# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2015 Francesco Ceruti <ceppofrancy@gmail.com>
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

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QTextEdit, \
    QSpinBox, QLabel

from lisp.ui.qcolorbutton import QColorButton
from lisp.ui.settings.section import SettingsSection


class Appearance(SettingsSection):

    Name = 'Appearance'

    def __init__(self, size, parent=None):
        super().__init__(size, parent)

        self.setLayout(QVBoxLayout())

        # Name
        self.textEditGroup = QGroupBox(self)
        self.textEditGroup.setLayout(QHBoxLayout())
        self.layout().addWidget(self.textEditGroup)

        self.textEdit = QTextEdit(self.textEditGroup)
        self.textEditGroup.layout().addWidget(self.textEdit)

        # Font
        self.fontSizeGroup = QGroupBox(self)
        self.fontSizeGroup.setLayout(QHBoxLayout())
        self.layout().addWidget(self.fontSizeGroup)

        self.fontSizeSpin = QSpinBox(self.fontSizeGroup)
        self.fontSizeSpin.setValue(QLabel().fontInfo().pointSize())
        self.fontSizeGroup.layout().addWidget(self.fontSizeSpin)

        # Color
        self.colorGroup = QGroupBox(self)
        self.colorGroup.setLayout(QHBoxLayout())
        self.layout().addWidget(self.colorGroup)

        self.colorBButton = QColorButton(self.colorGroup)
        self.colorFButton = QColorButton(self.colorGroup)

        self.colorGroup.layout().addWidget(self.colorBButton)
        self.colorGroup.layout().addWidget(self.colorFButton)

        # Warning
        self.warning = QLabel(self)
        self.warning.setText("The appearance depends on the layout")
        self.warning.setAlignment(QtCore.Qt.AlignCenter)
        self.warning.setStyleSheet("color: yellow; font-weight: bold")
        self.layout().addWidget(self.warning)

        # Set stretch
        self.layout().setStretch(0, 3)
        self.layout().setStretch(1, 1)
        self.layout().setStretch(2, 1)
        self.layout().setStretch(3, 1)

        self.retranslateUi()

    def retranslateUi(self):
        self.textEditGroup.setTitle("Shown Text")
        self.textEdit.setText("Empty")
        self.fontSizeGroup.setTitle("Set Font Size")
        self.colorGroup.setTitle("Color")
        self.colorBButton.setText("Select background color")
        self.colorFButton.setText("Select font color")

    def enable_check(self, enable):
        self.textEditGroup.setCheckable(enable)
        self.textEditGroup.setChecked(False)

        self.fontSizeGroup.setCheckable(enable)
        self.fontSizeGroup.setChecked(False)

        self.colorGroup.setCheckable(enable)
        self.colorGroup.setChecked(False)

    def get_configuration(self):
        conf = {}
        style = {}
        checked = self.textEditGroup.isCheckable()

        if not (checked and not self.textEditGroup.isChecked()):
            conf['name'] = self.textEdit.toPlainText()
        if not (checked and not self.colorGroup.isChecked()):
            if self.colorBButton.color() is not None:
                style['background'] = self.colorBButton.color()
            if self.colorFButton.color() is not None:
                style['color'] = self.colorFButton.color()
        if not (checked and not self.fontSizeGroup.isChecked()):
            style['font-size'] = str(self.fontSizeSpin.value()) + 'pt'

        if style:
            conf['stylesheet'] = dict_to_css(style)

        return conf

    def set_configuration(self, conf):
        if 'name' in conf:
            self.textEdit.setText(conf['name'])
        if 'stylesheet' in conf:
            conf = css_to_dict(conf['stylesheet'])
            if 'background' in conf:
                self.colorBButton.setColor(conf['background'])
            if 'color' in conf:
                self.colorFButton.setColor(conf['color'])
            if 'font-size' in conf:
                # [:-2] for removing "pt"
                self.fontSizeSpin.setValue(int(conf['font-size'][:-2]))


def css_to_dict(css):
    dict = {}
    css = css.strip()

    for attribute in css.split(';'):
        try:
            name, value = attribute.split(':')
            dict[name.strip()] = value.strip()
        except:
            pass

    return dict


def dict_to_css(css_dict):
    css = ''
    for name in css_dict:
        css += name + ':' + str(css_dict[name]) + ';'

    return css