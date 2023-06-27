"""
Custom Separator

    This class creates a separator that is similar to that of Maya's
"""

from tank.platform.qt5 import QtWidgets

class Separator(QtWidgets.QFrame):
    def __init__(self):
        """
        Constructor
        """
        super(Separator, self).__init__(parent=None)

        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setFixedHeight(1)
