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
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

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
        sg = self._app.shotgun

        # # create search widget
        # search_widget = global_search_widget.GlobalSearchWidget(self)
        # # give the search widget a handle on the task manager
        # search_widget.set_bg_task_manager(self._bg_task_manager)
        # # set the entity types to search through (this is also the default dict)
        # search_widget.set_searchable_entity_types(
        #     {
        #         "Asset": [],
        #         "Shot": [],
        #         "Task": [],
        #         # only active users
        #         "ClientUser": [["sg_status_list", "is", "act"]],
        #         "ApiUser": [],
        #         "Version": [],
        #         "PublishedFile": [],
        #     }
        # )

        # # display some instructions
        # info_lbl = QtGui.QLabel(
        #     "Click in the widget and type to search for Shotgun entities. You "
        #     "will need to type at least 3 characters before the search begins."
        # )

        # # create a label to show when an entity is activated
        # self._activated_label = QtGui.QLabel()
        # self._activated_label.setWordWrap(True)
        # self._activated_label.setStyleSheet(
        #     """
        #     QLabel {
        #         color: #18A7E3;
        #     }
        #     """
        # )

        # # lay out the UI
        # layout = QtGui.QVBoxLayout(self)
        # layout.setSpacing(16)
        # layout.addStretch()
        # layout.addWidget(info_lbl)
        # layout.addWidget(search_widget)
        # layout.addWidget(self._activated_label)
        # layout.addStretch()

        # # connect the entity activated singal
        # search_widget.entity_activated.connect(self._on_entity_activated)

        # Set up UI
        projectName = str(self._app.context).replace("Project ", "")
        self.ui.context.setText(projectName)

        localStorage = sg.find('LocalStorage', [], ['windows_path'])[0]['windows_path']

        tankName = sg.find('Project', [['name', 'is', str(projectName)]], ['tank_name'])[0]['tank_name']

        self.ui.packageButton.clicked.connect(self.startPackaging)
        
        self.playlistPackager = copy_from_playlist.PlaylistPacker(sg, projectName)

        outputPath = self.ui.outputDialogBtn.clicked.connect(self.selectDirDialog)

        # project_id = 91
        # tk = sgtk.sgtk_from_entity("Project", project_id)

        # self._apiHandel = sgtk.find('LocalStorage', [], ['windows_path'])[0]['windows_path']


    def addPlaylist(self):
        playlistName = self.ui.playlistInput.text()


    def startPackaging(self):
        playlistName = self.ui.playlistInput.text()
        self.ui.context.setText(playlistName)
        compress = self.compress.isChecked()
        self.playlistPackager.packagePlaylists([playlistName], compress)

    def selectDirDialog(self):
        selectedDir = QtGui.QFileDialog.getExistingDirectory(
            self,
            "Select a folder",
            self.playlistPackager.getProjectPath(),
            QtGui.QFileDialog.ShowDirsOnly
            )
        self.ui.outputPathText.setText(selectedDir)
        return selectedDir

    # def destroy(self):
    #     """Clean up the object when deleted."""
    #     self._bg_task_manager.shut_down()

    # def _on_entity_activated(self, entity_type, entity_id, entity_name):
    #     """Handle entity activated."""

    #     self._activated_label.setText(
    #         "<strong>%s</strong> '%s' with id <tt>%s</tt> activated" % (
    #             entity_type, entity_name, entity_id)
    #     )