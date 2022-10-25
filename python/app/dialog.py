# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
import threading
from . import copy_from_playlist
from pathlib import Path

# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

# import the global_search_widget module from the qtwidgets framework
global_search_widget = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "global_search_widget")

# import the task manager from shotgunutils framework
# task_manager = sgtk.platform.import_framework(
#     "tk-framework-shotgunutils", "task_manager")

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Copy From Playlist", app_instance, AppDialog)


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        # now load in the UI that was created in the UI designer
        # self.ui = Ui_Dialog()
        # Set up UI

        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        # create a bg task manager for pulling data from SG
        # self._bg_task_manager = task_manager.BackgroundTaskManager(self)

        # logging happens via a standard toolkit logger
        logger.info("Launching Copy From Playlist...")

        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - An Sgtk API instance, via self._app.sgtk

        # Shotgun API instance
        self.sg = self._app.shotgun

        self.projectName = str(self._app.context).replace("Project ", "")
        # self.ui.context.setText(self.projectName)

        self.localStorage = Path(self._app.sgtk.project_path).anchor.replace("\\", "/")

        self.playlistPackager = copy_from_playlist.PlaylistPacker(self.sg, self.projectName, self.localStorage)
        self.ui = self.playlistPackager.ui
        self.ui.setupUi(self)

        self.playlistInput = self.ui.playlistInput
        self.playlistnames = []
        self.playlistSelection = self.ui.playlistSelection
        self.getPlaylists()
        self.populate_playlist()
        self.playlistCount = len(self.playlistnames)
        self.currentPlaylist = None

        self.playlistSelection.clicked.connect(self.setPlaylist)
        self.playlistInput.textChanged.connect(self.searchPlaylist)
        self.ui.packageButton.clicked.connect(self.startPackaging)

        self.ui.outputDialogBtn.clicked.connect(self.selectDirDialog)
        #self.setDefaultPath()

    def getProjectPath(self):
        tankName = self.sg.find_one('Project', [['name', 'is', self.projectName]], ['tank_name'])['tank_name']
        projectPath = os.path.join(self.localStorage, tankName)
        self.log('PROJECT PATH: {}'.format(projectPath))
        return projectPath

    def setDefaultPath(self):
        projectDir = os.path.join(self.getProjectPath(), 'MyPlaylists')
        self.ui.outputPathText.setText(projectDir)

    def setPlaylist(self):
        self.currentPlaylist = self.playlistSelection.currentItem().text()
        self.ui.selectedPlaylistInput.setText(self.currentPlaylist)

    def searchPlaylist(self):
        self.playlistSelection.clear()
        prefix = self.ui.playlistInput.text()
        i = self.binary_search(self.playlistnames, prefix)

        for index in range(i, self.playlistCount):
            if self.playlistnames[index].startswith(prefix):
                self.playlistSelection.addItem(self.playlistnames[index])
            else:
                break

    def binary_search(self, array, target):
        lo = 0
        hi = len(array)

        while lo < hi:
            mid = (lo + hi) // 2
            if array[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def getPlaylists(self):
        """
        Get the playlists
        """
        self.playlists = self.sg.find("Playlist", [['project.Project.name', 'is', self.projectName]], ['code'])
        #self.log('### playlistids: %s' % self.playlists)

        for playlist in self.playlists:
            if playlist and playlist['code']:
                self.playlistnames.append(playlist["code"])
        self.playlistnames.sort()
        #self.log('### playlistnames: %s' % self.playlistnames)

    def populate_playlist(self):
        """
        Populate the playlist
        """
        playlistSelection = self.playlistSelection
        playlistSelection.clear()
        for playlist in self.playlistnames:
            playlistSelection.addItem(playlist)

    def addPlaylist(self):
        playlistName = self.ui.playlistInput.text()

    def startPackaging(self):
        if self.currentPlaylist:
            playlistName = self.currentPlaylist
            compress = self.ui.compress.isChecked()
            openFolder = self.ui.destinationFolder.isChecked()
            self.playlistPackager.packagePlaylists([playlistName], openFolder, compress, self.ui.outputPathText.text())
        else:
            self.log('No playlist is selected', error=1)

    def selectDirDialog(self):
        selectedDir = QtGui.QFileDialog.getExistingDirectory(
            self,
            "Select a folder",
            self.playlistPackager.getProjectPath(),
            QtGui.QFileDialog.ShowDirsOnly
            )
        self.ui.outputPathText.setText(selectedDir)
        return selectedDir

    def log(self, msg, error=0):
        if logger:
            if error:
                logger.warn(msg)
            else:
                logger.info(msg)

        print(msg)

    # def destroy(self):
    #     """Clean up the object when deleted."""
    #     self._bg_task_manager.shut_down()

    # def _on_entity_activated(self, entity_type, entity_id, entity_name):
    #     """Handle entity activated."""

    #     self._activated_label.setText(
    #         "<strong>%s</strong> '%s' with id <tt>%s</tt> activated" % (
    #             entity_type, entity_name, entity_id)
    #     )