# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/ui/dialogs/xml_preview.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.setWindowModality(QtCore.Qt.WindowModal)
        main_window.resize(600, 500)
        main_window.setMinimumSize(QtCore.QSize(600, 500))
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.xml_content = QtWidgets.QTextEdit(self.central_widget)
        self.xml_content.setReadOnly(True)
        self.xml_content.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.xml_content.setObjectName("xml_content")
        self.verticalLayout.addWidget(self.xml_content)
        main_window.setCentralWidget(self.central_widget)
        self.tool_bar = QtWidgets.QToolBar(main_window)
        self.tool_bar.setObjectName("tool_bar")
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.tool_bar)
        self.action_save = QtWidgets.QAction(main_window)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/img/icons/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_save.setIcon(icon)
        self.action_save.setObjectName("action_save")
        self.action_save_as = QtWidgets.QAction(main_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/img/icons/save_as.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_save_as.setIcon(icon1)
        self.action_save_as.setObjectName("action_save_as")
        self.tool_bar.addAction(self.action_save)
        self.tool_bar.addAction(self.action_save_as)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "XML Preview"))
        self.tool_bar.setWindowTitle(_translate("main_window", "Tools Bar"))
        self.action_save.setText(_translate("main_window", "Save"))
        self.action_save.setShortcut(_translate("main_window", "Ctrl+S"))
        self.action_save_as.setText(_translate("main_window", "Save As"))
        self.action_save_as.setToolTip(_translate("main_window", "Save As"))
        self.action_save_as.setShortcut(_translate("main_window", "Ctrl+Shift+S"))

import img_rc
