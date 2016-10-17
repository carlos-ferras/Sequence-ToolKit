# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/ui/widgets/custom_row_widget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_custom_row_widget(object):
    def setupUi(self, custom_row_widget):
        custom_row_widget.setObjectName("custom_row_widget")
        custom_row_widget.resize(429, 172)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(custom_row_widget.sizePolicy().hasHeightForWidth())
        custom_row_widget.setSizePolicy(sizePolicy)
        custom_row_widget.setMouseTracking(True)
        custom_row_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.gridLayout = QtWidgets.QGridLayout(custom_row_widget)
        self.gridLayout.setContentsMargins(20, 15, 20, 15)
        self.gridLayout.setHorizontalSpacing(80)
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        self.retranslateUi(custom_row_widget)
        QtCore.QMetaObject.connectSlotsByName(custom_row_widget)

    def retranslateUi(self, custom_row_widget):
        _translate = QtCore.QCoreApplication.translate
        custom_row_widget.setWindowTitle(_translate("custom_row_widget", "CustomRowWidget"))

