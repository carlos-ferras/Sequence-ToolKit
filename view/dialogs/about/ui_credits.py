# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/ui/dialogs/about/credits.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_credits(object):
    def setupUi(self, credits):
        credits.setObjectName("credits")
        credits.resize(666, 350)
        credits.setMinimumSize(QtCore.QSize(666, 350))
        self.verticalLayout = QtWidgets.QVBoxLayout(credits)
        self.verticalLayout.setObjectName("verticalLayout")
        self.credits_label = QtWidgets.QLabel(credits)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.credits_label.setFont(font)
        self.credits_label.setStyleSheet("font-size:34px")
        self.credits_label.setAlignment(QtCore.Qt.AlignCenter)
        self.credits_label.setObjectName("credits_label")
        self.verticalLayout.addWidget(self.credits_label)
        self.credits_text = QtWidgets.QTextEdit(credits)
        self.credits_text.setReadOnly(True)
        self.credits_text.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.credits_text.setObjectName("credits_text")
        self.verticalLayout.addWidget(self.credits_text)

        self.retranslateUi(credits)
        QtCore.QMetaObject.connectSlotsByName(credits)

    def retranslateUi(self, credits):
        _translate = QtCore.QCoreApplication.translate
        credits.setWindowTitle(_translate("credits", "credits"))
        self.credits_label.setText(_translate("credits", "Credits"))
        self.credits_text.setHtml(_translate("credits", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Bitstream Charter\'; font-size:12pt; font-weight:600;\">This application is the result of the collaboration between the department of free software from the University of Informatics Sciences (UCI) in Havana and the Luminescence Dating Laboratory at CEADEN.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Bitstream Charter\'; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Bitstream Charter\'; font-size:10pt; font-weight:600;\">Created and Designed by:</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Bitstream Charter\'; font-size:12pt; font-weight:600;\">Carlos Manuel Ferrás Hernández</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Bitstream Charter\'; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Bitstream Charter\'; font-size:10pt; font-weight:600;\">Documented by:</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Bitstream Charter\'; font-size:12pt; font-weight:600;\">Yanet Leonor Quesada Hernández</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Bitstream Charter\'; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Bitstream Charter\'; font-size:10pt; font-weight:600;\">XML structure and concepts:</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Bitstream Charter\'; font-size:12pt; font-weight:600;\">Luis Baly Gil</span></p></body></html>"))

