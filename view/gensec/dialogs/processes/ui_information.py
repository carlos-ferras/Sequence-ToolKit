# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'information.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_process(object):
    def setupUi(self, process):
        process.setObjectName("process")
        process.resize(381, 112)
        process.setMinimumSize(QtCore.QSize(0, 112))
        process.setMaximumSize(QtCore.QSize(16777215, 112))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(process)
        self.horizontalLayout_3.setSpacing(12)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.form_area = QtWidgets.QFrame(process)
        self.form_area.setFrameShape(QtWidgets.QFrame.Box)
        self.form_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.form_area.setObjectName("form_area")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.form_area)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setObjectName("layout")
        self.date_type_label = QtWidgets.QLabel(self.form_area)
        self.date_type_label.setObjectName("date_type_label")
        self.layout.addWidget(self.date_type_label)
        self.date_type = QtWidgets.QLineEdit(self.form_area)
        self.date_type.setMinimumSize(QtCore.QSize(150, 28))
        self.date_type.setObjectName("date_type")
        self.layout.addWidget(self.date_type)
        self.verticalLayout_2.addLayout(self.layout)
        self.layout_2 = QtWidgets.QHBoxLayout()
        self.layout_2.setObjectName("layout_2")
        self.comments_label = QtWidgets.QLabel(self.form_area)
        self.comments_label.setObjectName("comments_label")
        self.layout_2.addWidget(self.comments_label)
        self.comments = QtWidgets.QLineEdit(self.form_area)
        self.comments.setMinimumSize(QtCore.QSize(150, 28))
        self.comments.setObjectName("comments")
        self.layout_2.addWidget(self.comments)
        self.verticalLayout_2.addLayout(self.layout_2)
        self.horizontalLayout_3.addWidget(self.form_area)
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
        self.verticalLayout = QtWidgets.QVBoxLayout(self.buttons_area)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.push_button_accept = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_accept.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_accept.setShortcut("Return")
        self.push_button_accept.setObjectName("push_button_accept")
        self.verticalLayout.addWidget(self.push_button_accept)
        self.push_button_cancel = QtWidgets.QPushButton(self.buttons_area)
        self.push_button_cancel.setMinimumSize(QtCore.QSize(100, 32))
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.verticalLayout.addWidget(self.push_button_cancel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.buttons_area)

        self.retranslateUi(process)
        QtCore.QMetaObject.connectSlotsByName(process)

    def retranslateUi(self, process):
        _translate = QtCore.QCoreApplication.translate
        process.setWindowTitle(_translate("process", "Information"))
        self.date_type_label.setText(_translate("process", "Date Type"))
        self.comments_label.setText(_translate("process", "Comments"))
        self.push_button_accept.setText(_translate("process", "Accept"))
        self.push_button_cancel.setText(_translate("process", "Cancel"))
        self.push_button_cancel.setShortcut(_translate("process", "Esc"))

