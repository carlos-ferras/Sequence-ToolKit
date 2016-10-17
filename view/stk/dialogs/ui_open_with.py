    # -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/ui/stk/dialogs/open_with.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_open_with(object):
    def setupUi(self, open_with):
        open_with.setObjectName("open_with")
        open_with.resize(267, 110)
        self.verticalLayout = QtWidgets.QVBoxLayout(open_with)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.push_button_gensec = QtWidgets.QPushButton(open_with)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_gensec.sizePolicy().hasHeightForWidth())
        self.push_button_gensec.setSizePolicy(sizePolicy)
        self.push_button_gensec.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.push_button_gensec.setFont(font)
        self.push_button_gensec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.push_button_gensec.setStyleSheet("text-align: left")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/img/logos/gensec.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_gensec.setIcon(icon)
        self.push_button_gensec.setIconSize(QtCore.QSize(30, 30))
        self.push_button_gensec.setObjectName("push_button_gensec")
        self.verticalLayout.addWidget(self.push_button_gensec)
        self.push_button_genrep = QtWidgets.QPushButton(open_with)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_genrep.sizePolicy().hasHeightForWidth())
        self.push_button_genrep.setSizePolicy(sizePolicy)
        self.push_button_genrep.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.push_button_genrep.setFont(font)
        self.push_button_genrep.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.push_button_genrep.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.push_button_genrep.setStyleSheet("text-align: left")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/img/logos/genrep.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.push_button_genrep.setIcon(icon1)
        self.push_button_genrep.setIconSize(QtCore.QSize(30, 30))
        self.push_button_genrep.setObjectName("push_button_genrep")
        self.verticalLayout.addWidget(self.push_button_genrep)

        self.retranslateUi(open_with)
        QtCore.QMetaObject.connectSlotsByName(open_with)

    def retranslateUi(self, open_with):
        _translate = QtCore.QCoreApplication.translate
        open_with.setWindowTitle(_translate("open_with", "Open With?"))
        self.push_button_gensec.setText(_translate("open_with", "GenSec"))
        self.push_button_genrep.setText(_translate("open_with", "GenRep"))

import img_rc
