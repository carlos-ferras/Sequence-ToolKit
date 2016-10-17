#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtCore, QtGui

from controller.dialogs.about.about import About


class AboutSTK(About):
    def __init__(self, parent=None):
        About.__init__(self, parent)

        self.setWindowTitle(QtCore.QCoreApplication.translate('about', 'About {0}').format('Sequence-ToolKit'))
        self.app_name.setText('Sequence-ToolKit')
        self.short_description.setText(QtCore.QCoreApplication.translate('about', 'Sequence Management Package'))
        self.version.setText('3.0.0')
        self.long_description.setText(QtCore.QCoreApplication.translate(
            'about',
            'Is a Free-Open-Source Applications-Package used in the generation and posterior analysis of the '
            'measurement sequences for automated luminescence reader LF02. Was programmed on the '
            'basis of technical task elaborated by the LF02 developers.'
        ))
        self.app_icon.setScaledContents(True)
        self.app_icon.setPixmap(QtGui.QPixmap(":/resources/img/logos/sequence_toolkit.svg"))
