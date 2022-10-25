# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!


from tank.platform.qt import QtCore, QtGui
from tank.platform.qt5 import QtWidgets
#from qgis.PyQt.QtWidgets import QVBoxLayout
from . import separator


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        app = QtWidgets.QApplication.instance()
        app.processEvents()

        Dialog.setObjectName("Dialog")
        #Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #Dialog.resize(431, 392)
        Dialog.resize(489, 792)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.layout().setContentsMargins(15, 20, 15, 10)

        # Search Layout
        self.inputLayout = QtGui.QVBoxLayout(Dialog)
        self.inputLayout.setObjectName("inputLayout")

        self.searchLabel = QtGui.QLabel(Dialog)
        self.searchLabel.setObjectName("context")
        self.searchLabel.setText("Search")

        self.playlistInput = QtGui.QLineEdit(Dialog)
        self.playlistInput.setPlaceholderText("Playlist name...")
        self.playlistInput.setToolTip('Enter the first few characters of query playlist name (case sensitive)')

        self.inputLayout.addWidget(self.searchLabel)
        self.inputLayout.addWidget(self.playlistInput)
        self.verticalLayout.addLayout(self.inputLayout)

        # Playlists Layout
        self.playlistLayout = QtGui.QVBoxLayout(Dialog)
        #self.playlistLayout.layout().setContentsMargins(0, 5, 0, 30)
        self.playlistLabel = QtGui.QLabel(Dialog)
        self.playlistLabel.setText("Playlists")

        self.playlistSelection = QtWidgets.QListWidget()
        self.playlistSelection.setToolTip('Select a playlist')

        self.playlistLayout.addWidget(self.playlistLabel)
        self.playlistLayout.addWidget(self.playlistSelection)
        self.verticalLayout.addLayout(self.playlistLayout)

        # Selected Playlist Layout
        self.selectedPlaylistLayout = QtGui.QVBoxLayout(Dialog)
        self.selectedPlaylistLayout.layout().setContentsMargins(0, 0, 0, 20)
        self.selectedPlaylistLabel = QtGui.QLabel(Dialog)
        self.selectedPlaylistLabel.setText("Selected Playlist")

        self.selectedPlaylistInput = QtGui.QLineEdit(Dialog)
        self.selectedPlaylistInput.setPlaceholderText("Selected playlist name...")
        self.selectedPlaylistInput.setToolTip('Display the playlist selected above')

        self.playlistLayout.addWidget(self.selectedPlaylistLabel)
        self.playlistLayout.addWidget(self.selectedPlaylistInput)
        self.verticalLayout.addLayout(self.selectedPlaylistLayout)

        #self_playlist_separator = separator.Separator()
        #self.verticalLayout.addWidget(self_playlist_separator)

        #Output Layout
        self.outputLayout = QtGui.QVBoxLayout(Dialog)
        self.outputLabel = QtGui.QLabel(Dialog)
        self.outputLabel.setText("Output")

        self.fileLayout = QtGui.QHBoxLayout(Dialog)
        self.outputPathText = QtGui.QLineEdit()
        self.outputPathText.setPlaceholderText("Enter destination folder ")
        self.outputPathText.setToolTip('Use default destination folder B:\Ark2Depot\MyPlaylists or enter a new one')
        self.outputDialogBtn = QtGui.QPushButton()
        self.outputDialogBtn.setText("Select a folder")
        self.outputDialogBtn.setToolTip('Override default or entered destination folder')
        self.fileLayout.addWidget(self.outputPathText)
        self.fileLayout.addWidget(self.outputDialogBtn)

        self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.fileLayout)
        self.verticalLayout.addLayout(self.outputLayout)

        # Output Layout
        self.optionsLayout = QtGui.QHBoxLayout(Dialog)
        self.destinationFolder = QtGui.QCheckBox()
        self.destinationFolder.setText("Open destination folder")
        self.destinationFolder.setToolTip('If checked, destination folder will be opened as soon as you click on \"Package Files\" button below')
        self.destinationFolder.setChecked(True)

        self.compress = QtGui.QCheckBox()
        self.compress.setText("Zip files once complete")
        self.compress.setToolTip('If checked, destination folder will be zipped once all playlist files have been copied or downloaded to destination folder')
        #self.compress.setChecked(True)
        self.compress.setChecked(False)

        self.optionsLayout.addWidget(self.destinationFolder)
        self.optionsLayout.addWidget(self.compress)

        self.verticalLayout.addLayout(self.optionsLayout)

        # Package Layout
        self.packageLayout = QtGui.QVBoxLayout(Dialog)
        self.packageLayout.layout().setContentsMargins(0, 0, 0, 25)
        self.packageButton = QtGui.QPushButton()
        self.packageButton.setText("Package Files")
        self.packageButton.setToolTip('Copy or download playlist files to the destination folder. Check above if you want to open or zip destination folder.')
        self.packageLayout.addWidget(self.packageButton)
        self.verticalLayout.addLayout(self.packageLayout)

        # Status Layout
        self.statusLayout = QtGui.QVBoxLayout(Dialog)
        self.statusLayout.layout().setContentsMargins(0, 0, 0, 10)
        self.progressLabel = QtGui.QLabel(Dialog)
        self.progressLabel.setText("Progress")

        self.status_dialog = QtWidgets.QTextBrowser(Dialog)
        self.status_dialog.verticalScrollBar().setValue(self.status_dialog.verticalScrollBar().maximum())
        self.status_dialog.setMinimumHeight(200)

        self.statusLayout.addWidget(self.progressLabel)
        self.statusLayout.addWidget(self.status_dialog)
        self.verticalLayout.addLayout(self.statusLayout)

        # Progress Layout
        self.progressLayout = QtGui.QVBoxLayout(Dialog)
        self.progressLayout.layout().setContentsMargins(0, 0, 0, 20)

        self.FilesProgressBar = QtGui.QProgressBar()
        self.progressLayout.addWidget(self.FilesProgressBar)
        """
        self.FilesProgressBar.setStyleSheet(
            '''
            QWidget
            {
                color: #b1b1b1;
                background-color: #323232;
            }
            QProgressBar
            {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk
            {
                background-color: #d7801a;
                width: 2.15px;
                margin: 0.5px;
            }
            
            '''
        )
        """

        #self.progress.setGeometry(200, 80, 250, 20)

        self.verticalLayout.addLayout(self.progressLayout)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        #self.context.setText(QtGui.QApplication.translate("Dialog", "Your Current Context: ", None, QtGui.QApplication.UnicodeUTF8))


from . import resources_rc
