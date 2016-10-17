# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/ui/genrep/dialogs/profile.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_profile(object):
    def setupUi(self, profile):
        profile.setObjectName("profile")
        profile.resize(519, 248)
        self.horizontalLayout = QtWidgets.QHBoxLayout(profile)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.form_area = QtWidgets.QFrame(profile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.form_area.sizePolicy().hasHeightForWidth())
        self.form_area.setSizePolicy(sizePolicy)
        self.form_area.setFrameShape(QtWidgets.QFrame.Box)
        self.form_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.form_area.setObjectName("form_area")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.form_area)
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.all_parameters = QtWidgets.QCheckBox(self.form_area)
        self.all_parameters.setObjectName("all_parameters")
        self.verticalLayout.addWidget(self.all_parameters)
        self.parameters_list = QtWidgets.QListWidget(self.form_area)
        self.parameters_list.setObjectName("parameters_list")
        self.verticalLayout.addWidget(self.parameters_list)
        self.horizontalLayout.addWidget(self.form_area)
        self.buttons_area = QtWidgets.QFrame(profile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons_area.sizePolicy().hasHeightForWidth())
        self.buttons_area.setSizePolicy(sizePolicy)
        self.buttons_area.setMinimumSize(QtCore.QSize(128, 0))
        self.buttons_area.setMaximumSize(QtCore.QSize(128, 16777215))
        self.buttons_area.setFrameShape(QtWidgets.QFrame.Box)
        self.buttons_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttons_area.setObjectName("buttons_area")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.buttons_area)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.push_button_accept = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_accept.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_accept.setObjectName("push_button_accept")
        self.verticalLayout_2.addWidget(self.push_button_accept)
        self.push_button_cancel = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_cancel.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.verticalLayout_2.addWidget(self.push_button_cancel)
        self.push_button_load = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_load.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_load.setObjectName("push_button_load")
        self.verticalLayout_2.addWidget(self.push_button_load)
        self.push_button_save = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_save.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_save.setObjectName("push_button_save")
        self.verticalLayout_2.addWidget(self.push_button_save)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.buttons_area)

        self.retranslateUi(profile)
        QtCore.QMetaObject.connectSlotsByName(profile)

    def retranslateUi(self, profile):
        _translate = QtCore.QCoreApplication.translate
        profile.setWindowTitle(_translate("profile", "Profile"))
        self.all_parameters.setText(_translate("profile", "Parameters"))
        self.push_button_accept.setText(_translate("profile", "Accept"))
        self.push_button_cancel.setText(_translate("profile", "Cancel"))
        self.push_button_load.setText(_translate("profile", "Load"))
        self.push_button_save.setText(_translate("profile", "Save"))

