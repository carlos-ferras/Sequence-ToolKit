# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pause.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_process(object):
    def setupUi(self, process):
        process.setObjectName("process")
        process.resize(312, 164)
        process.setMinimumSize(QtCore.QSize(0, 164))
        process.setMaximumSize(QtCore.QSize(16777215, 164))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(process)
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.form_area = QtWidgets.QFrame(process)
        self.form_area.setFrameShape(QtWidgets.QFrame.Box)
        self.form_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.form_area.setObjectName("form_area")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.form_area)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.time_label = QtWidgets.QLabel(self.form_area)
        self.time_label.setObjectName("time_label")
        self.horizontalLayout.addWidget(self.time_label)
        self.time = QtWidgets.QDoubleSpinBox(self.form_area)
        self.time.setMinimumSize(QtCore.QSize(80, 28))
        self.time.setMaximumSize(QtCore.QSize(80, 16777215))
        self.time.setMaximum(99999.0)
        self.time.setObjectName("time")
        self.horizontalLayout.addWidget(self.time)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.form_area)
        self.buttons_area = QtWidgets.QFrame(process)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons_area.sizePolicy().hasHeightForWidth())
        self.buttons_area.setSizePolicy(sizePolicy)
        self.buttons_area.setMinimumSize(QtCore.QSize(0, 0))
        self.buttons_area.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.buttons_area.setFrameShape(QtWidgets.QFrame.Box)
        self.buttons_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttons_area.setObjectName("buttons_area")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.buttons_area)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.push_button_accept = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_accept.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_accept.setShortcut("Return")
        self.push_button_accept.setObjectName("push_button_accept")
        self.verticalLayout_2.addWidget(self.push_button_accept)
        self.push_button_cancel = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_cancel.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_cancel.setShortcut("Esc")
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.verticalLayout_2.addWidget(self.push_button_cancel)
        self.push_button_information = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_information.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_information.setObjectName("push_button_information")
        self.verticalLayout_2.addWidget(self.push_button_information)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.buttons_area)

        self.retranslateUi(process)
        QtCore.QMetaObject.connectSlotsByName(process)

    def retranslateUi(self, process):
        _translate = QtCore.QCoreApplication.translate
        process.setWindowTitle(_translate("process", "Pause"))
        self.time_label.setText(_translate("process", "Time (s)"))
        self.push_button_accept.setText(_translate("process", "Accept"))
        self.push_button_cancel.setText(_translate("process", "Cancel"))
        self.push_button_information.setText(_translate("process", "Information"))

