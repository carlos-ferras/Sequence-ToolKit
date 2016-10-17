# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/ui/widgets/custom_row_widget_item.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_custom_row_widget_item(object):
    def setupUi(self, custom_row_widget_item):
        custom_row_widget_item.setObjectName("custom_row_widget_item")
        custom_row_widget_item.resize(170, 196)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(custom_row_widget_item.sizePolicy().hasHeightForWidth())
        custom_row_widget_item.setSizePolicy(sizePolicy)
        custom_row_widget_item.setMinimumSize(QtCore.QSize(170, 0))
        custom_row_widget_item.setMaximumSize(QtCore.QSize(170, 16777215))
        custom_row_widget_item.setMouseTracking(True)
        custom_row_widget_item.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.verticalLayout = QtWidgets.QVBoxLayout(custom_row_widget_item)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setObjectName("layout")
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)
        self.file_icon = QtWidgets.QLabel(custom_row_widget_item)
        self.file_icon.setMinimumSize(QtCore.QSize(130, 170))
        self.file_icon.setMaximumSize(QtCore.QSize(130, 170))
        self.file_icon.setMouseTracking(True)
        self.file_icon.setText("")
        self.file_icon.setScaledContents(True)
        self.file_icon.setObjectName("file_icon")
        self.layout.addWidget(self.file_icon)
        spacerItem1 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.layout)
        self.path = QtWidgets.QLabel(custom_row_widget_item)
        self.path.setText("")
        self.path.setAlignment(QtCore.Qt.AlignCenter)
        self.path.setObjectName("path")
        self.verticalLayout.addWidget(self.path)
        self.action_properties = QtWidgets.QAction(custom_row_widget_item)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/img/icons/properties.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_properties.setIcon(icon)
        self.action_properties.setObjectName("action_properties")

        self.retranslateUi(custom_row_widget_item)
        QtCore.QMetaObject.connectSlotsByName(custom_row_widget_item)

    def retranslateUi(self, custom_row_widget_item):
        _translate = QtCore.QCoreApplication.translate
        custom_row_widget_item.setWindowTitle(_translate("custom_row_widget_item", "CustomRowWidgetItem"))
        self.action_properties.setText(_translate("custom_row_widget_item", "Properties"))

import img_rc
