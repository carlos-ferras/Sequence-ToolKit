#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtCore, QtGui

from controller.dialogs.about.about import About


class AboutGenRep(About):
    def __init__(self, parent=None):
        About.__init__(self, parent)

        self.setWindowTitle(QtCore.QCoreApplication.translate('about', 'About {0}').format('GenRep'))
        self.app_name.setText('GenRep')
        self.short_description.setText(QtCore.QCoreApplication.translate('about', 'Report Generator'))
        self.version.setText('3.2.0')
        self.long_description.setText(QtCore.QCoreApplication.translate(
            'about',
            'Is intended to produce a report on the basis of the data measured in the LF02 '
            'automated luminescence reader stored in a xml file (.SLF). The report may be generated in '
            'a xml file (.RLF) or as an exel file (.TXT).'
        ))
        self.app_icon.setScaledContents(True)
        self.app_icon.setPixmap(QtGui.QPixmap(":/resources/img/logos/genrep.svg"))
