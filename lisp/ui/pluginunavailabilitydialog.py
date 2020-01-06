# This file is part of Linux Show Player
#
# Copyright 2020 Francesco Ceruti <ceppofrancy@gmail.com>
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

from enum import Enum, auto

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from lisp.plugins import get_plugin, plugin_exists, plugin_status_icon
from lisp.ui.icons import IconTheme
from lisp.ui.ui_utils import translate

class PluginUnavailabilityDialogAction(Enum):
    NewShowfile = 101
    OpenDifferent = auto()

class PluginUnavailabilityDialog(QDialog):
    def __init__(self, plugin_list, **kwargs):
        super().__init__(**kwargs)

        self.setWindowTitle(translate("PluginUnavailabilityDialog", "Unable to load showfile"))
        self.setMinimumSize(400, 480)
        self.resize(400, 480)
        self.setLayout(QVBoxLayout(self))

        self.summaryText = QLabel(self)
        self.summaryText.setWordWrap(True)
        self.summaryText.setText(translate("PluginUnavailabilityDialog", "The showfile you are attempting to open uses plugins that are either:\n\n • Not installed on this system,\n • Have been disabled, or\n • Cannot be loaded due to a critical error.\n\nAs such, this showfile cannot be currently opened."))
        self.layout().addWidget(self.summaryText)

        self.pluginGroup = QGroupBox(self)
        self.pluginGroup.setTitle(translate("PluginUnavailabilityDialog", "Required Plugins"))
        self.pluginGroup.setLayout(QVBoxLayout(self.pluginGroup))

        # List of Plugins, with status indicators
        self.pluginList = QListWidget(self)
        self._font_height = self.pluginList.fontMetrics().height()
        self.pluginList.setSelectionMode(QAbstractItemView.NoSelection)
        self.pluginList.setIconSize(QSize(12, 12))
        for identifier, plugin in plugin_list.items():
            new_item = QListWidgetItem(
                self.getIndicator(identifier),
                translate(
                    "PluginUnavailabilityDialog", "{} ({} {})"
                ).format(
                    self.getName(identifier, plugin), identifier, self.getVersionText(identifier, plugin)
                )
            )
            new_item.setToolTip(self.getToolTip(identifier))
            self.pluginList.addItem(new_item)
        self.pluginGroup.layout().addWidget(self.pluginList)
        self.layout().addWidget(self.pluginGroup)

        # Buttons
        self.newButton = QPushButton(self)
        self.newButton.setText(translate('PluginUnavailabilityDialog', 'New showfile'))
        self.newButton.setIcon(IconTheme.get('document-new-symbolic'))
        self.newButton.clicked.connect(self._new)

        self.openButton = QPushButton(self)
        self.openButton.setText(translate('PluginUnavailabilityDialog', 'Open other'))
        self.openButton.setIcon(IconTheme.get('document-open'))
        self.openButton.clicked.connect(self._open)

        self.dialogButtons = QDialogButtonBox(self)
        self.dialogButtons.addButton(self.newButton, QDialogButtonBox.ActionRole)
        self.dialogButtons.addButton(self.openButton, QDialogButtonBox.ActionRole)
        self.dialogButtons.addButton(QDialogButtonBox.Cancel)
        self.layout().addWidget(self.dialogButtons)

        self.dialogButtons.rejected.connect(self.reject)

    def getIndicator(self, identifier):
        if not plugin_exists(identifier):
            return IconTheme.get('led-error-outline')
        return IconTheme.get(plugin_status_icon(get_plugin(identifier)))

    def getName(self, identifier, plugin):
        if not plugin_exists(identifier):
            return plugin['name']
        return get_plugin(identifier).Name

    def getToolTip(self, identifier):
        if not plugin_exists(identifier):
            return translate('PluginsTooltip', 'Plugin not installed.')
        return get_plugin(identifier).status_text()

    def getVersionText(self, identifier, plugin):
        if plugin_exists(identifier):
            vers_installed = get_plugin(identifier).Config.get('_version_', 0)
            if vers_installed != plugin['vers']:
                return translate('PluginUnavailabilityDialog', 'v{} (Installed: v{})').format(plugin['vers'], vers_installed)
        return translate('PluginUnavailabilityDialog', 'v{}').format(plugin['vers'])

    def _new(self):
        self.done(PluginUnavailabilityDialogAction.NewShowfile.value)

    def _open(self):
        self.done(PluginUnavailabilityDialogAction.OpenDifferent.value)
