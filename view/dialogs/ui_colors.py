# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/ui/dialogs/colors.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_color_dialog(object):
    def setupUi(self, color_dialog):
        color_dialog.setObjectName("color_dialog")
        color_dialog.resize(316, 199)
        self.verticalLayout = QtWidgets.QVBoxLayout(color_dialog)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setSpacing(25)
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setSpacing(10)
        self.vertical_layout.setObjectName("vertical_layout")
        self.color1_label = QtWidgets.QLabel(color_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color1_label.sizePolicy().hasHeightForWidth())
        self.color1_label.setSizePolicy(sizePolicy)
        self.color1_label.setObjectName("color1_label")
        self.vertical_layout.addWidget(self.color1_label)
        self.color1 = QtWidgets.QLabel(color_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color1.sizePolicy().hasHeightForWidth())
        self.color1.setSizePolicy(sizePolicy)
        self.color1.setMinimumSize(QtCore.QSize(80, 80))
        self.color1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.color1.setText("")
        self.color1.setObjectName("color1")
        self.vertical_layout.addWidget(self.color1)
        self.horizontal_layout.addLayout(self.vertical_layout)
        self.vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.vertical_layout_2.setSpacing(10)
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.color2_label = QtWidgets.QLabel(color_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color2_label.sizePolicy().hasHeightForWidth())
        self.color2_label.setSizePolicy(sizePolicy)
        self.color2_label.setObjectName("color2_label")
        self.vertical_layout_2.addWidget(self.color2_label)
        self.color2 = QtWidgets.QLabel(color_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color2.sizePolicy().hasHeightForWidth())
        self.color2.setSizePolicy(sizePolicy)
        self.color2.setMinimumSize(QtCore.QSize(80, 80))
        self.color2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.color2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.color2.setText("")
        self.color2.setObjectName("color2")
        self.vertical_layout_2.addWidget(self.color2)
        self.horizontal_layout.addLayout(self.vertical_layout_2)
        self.vertical_layout_3 = QtWidgets.QVBoxLayout()
        self.vertical_layout_3.setSpacing(10)
        self.vertical_layout_3.setObjectName("vertical_layout_3")
        self.color3_label = QtWidgets.QLabel(color_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color3_label.sizePolicy().hasHeightForWidth())
        self.color3_label.setSizePolicy(sizePolicy)
        self.color3_label.setObjectName("color3_label")
        self.vertical_layout_3.addWidget(self.color3_label)
        self.color3 = QtWidgets.QLabel(color_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color3.sizePolicy().hasHeightForWidth())
        self.color3.setSizePolicy(sizePolicy)
        self.color3.setMinimumSize(QtCore.QSize(80, 80))
        self.color3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.color3.setText("")
        self.color3.setObjectName("color3")
        self.vertical_layout_3.addWidget(self.color3)
        self.horizontal_layout.addLayout(self.vertical_layout_3)
        self.verticalLayout.addLayout(self.horizontal_layout)
        self.line = QtWidgets.QFrame(color_dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.buttons_area = QtWidgets.QHBoxLayout()
        self.buttons_area.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.buttons_area.setSpacing(10)
        self.buttons_area.setObjectName("buttons_area")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_area.addItem(spacerItem)
        self.push_button_accept = QtWidgets.QPushButton(color_dialog)
        self.push_button_accept.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_accept.setObjectName("push_button_accept")
        self.buttons_area.addWidget(self.push_button_accept)
        self.push_button_cancel = QtWidgets.QPushButton(color_dialog)
        self.push_button_cancel.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.buttons_area.addWidget(self.push_button_cancel)
        self.verticalLayout.addLayout(self.buttons_area)

        self.retranslateUi(color_dialog)
        QtCore.QMetaObject.connectSlotsByName(color_dialog)

    def retranslateUi(self, color_dialog):
        _translate = QtCore.QCoreApplication.translate
        color_dialog.setWindowTitle(_translate("color_dialog", "Select Colors"))
        self.color1_label.setText(_translate("color_dialog", "Color 1"))
        self.color1.setToolTip(_translate("color_dialog", "Double click to change the color"))
        self.color2_label.setText(_translate("color_dialog", "Color 2"))
        self.color2.setToolTip(_translate("color_dialog", "Double click to change the color"))
        self.color3_label.setText(_translate("color_dialog", "Color 3"))
        self.color3.setToolTip(_translate("color_dialog", "Double click to change the color"))
        self.push_button_accept.setText(_translate("color_dialog", "Accept"))
        self.push_button_cancel.setText(_translate("color_dialog", "Cancel"))

