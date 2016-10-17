#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtCore, QtGui

from controller.dialogs.about.about import About


class AboutGenSec(About):
    def __init__(self, parent=None):
        About.__init__(self, parent)

        self.setWindowTitle(QtCore.QCoreApplication.translate('about', 'About {0}').format('GenSec'))
        self.app_name.setText('GenSec')
        self.short_description.setText(QtCore.QCoreApplication.translate('about', 'Sequence Generator'))
        self.version.setText('3.0.0')
        self.long_description.setText(QtCore.QCoreApplication.translate(
            'about',
            'Generates a xml file (.SLF) with the data used by the LF02 automated luminescence '
            'reader to run a measuring sequence.'
        ))
        self.app_icon.setScaledContents(True)
        self.app_icon.setPixmap(QtGui.QPixmap(":/resources/img/logos/gensec.svg"))
