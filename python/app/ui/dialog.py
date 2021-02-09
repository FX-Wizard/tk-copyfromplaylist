# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(431, 392)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)

        # self.logo_example = QtGui.QLabel(Dialog)
        # self.logo_example.setText("")
        # self.logo_example.setPixmap(QtGui.QPixmap(":/res/sg_logo.png"))
        # self.logo_example.setObjectName("logo_example")
        # self.horizontalLayout.addWidget(self.logo_example)
        self.context = QtGui.QLabel(Dialog)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.context.sizePolicy().hasHeightForWidth())
        # self.context.setSizePolicy(sizePolicy)
        # self.context.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.context.setObjectName("context")
        self.horizontalLayout.addWidget(self.context)

        # playlist input
        self.inputLabel = QtGui.QLabel(Dialog)
        self.inputLabel.setObjectName("context")
        self.inputLabel.setText("Enter playlist name")
        self.verticalLayout.addWidget(self.inputLabel)
        # playlist input section
        self.inputLayout = QtGui.QHBoxLayout(Dialog)
        self.inputLayout.setObjectName("inputLayout")
        self.verticalLayout.addLayout(self.inputLayout)
        self.playlistInput = QtGui.QLineEdit()
        self.playlistInput.setPlaceholderText("Playlist name...")
        self.inputLayout.addWidget(self.playlistInput)
        self.addPlaylistBtn = QtGui.QPushButton()
        self.addPlaylistBtn.setText("+")
        self.inputLayout.addWidget(self.addPlaylistBtn)

        # options
        self.optionsLabel = QtGui.QLabel()
        self.optionsLabel.setText("Advanced Options")
        self.verticalLayout.addWidget(self.optionsLabel)

        self.useCustomPath = QtGui.QCheckBox()
        self.useCustomPath.setText("Save files to custom path")
        self.useCustomPath.setChecked(False)
        self.verticalLayout.addWidget(self.useCustomPath)

        self.outputLayout = QtGui.QHBoxLayout(Dialog)
        self.outputPathText = QtGui.QLineEdit()
        self.outputPathText.setPlaceholderText("Save location...")
        self.outputDialogBtn = QtGui.QPushButton()
        self.outputDialogBtn.setText("...")
        self.outputLayout.addWidget(self.outputPathText)
        self.outputLayout.addWidget(self.outputDialogBtn)
        self.verticalLayout.addLayout(self.outputLayout)

        # self.packageButton = QtGui.QPushButton()
        # self.packageButton.setText("OPEN")
        # self.verticalLayout.addWidget(self.packageButton)

        self.compress = QtGui.QCheckBox()
        self.compress.setText("Zip files once complete")
        self.compress.setChecked(True)
        self.verticalLayout.addWidget(self.compress)

        # package button
        self.packageButton = QtGui.QPushButton()
        self.packageButton.setText("PACKAGE")
        self.verticalLayout.addWidget(self.packageButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.context.setText(QtGui.QApplication.translate("Dialog", "Your Current Context: ", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
