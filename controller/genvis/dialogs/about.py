#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtCore, QtGui

from controller.dialogs.about.about import About


class AboutGenVis(About):
    def __init__(self, parent=None):
        About.__init__(self, parent)

        self.setWindowTitle(QtCore.QCoreApplication.translate('about', 'About {0}').format('GenVis'))
        self.app_name.setText('GenVis')
        self.short_description.setText(QtCore.QCoreApplication.translate('about', 'Report Analyzer'))
        self.version.setText('1.0.1')
        self.long_description.setText(QtCore.QCoreApplication.translate(
            'about',
            'Perform the analysis of the results obtained from the automated luminescence reader LF02, '
            'based on the report exported by the GenRep.'
        ))
        self.app_icon.setScaledContents(True)
        self.app_icon.setPixmap(QtGui.QPixmap(":/resources/img/logos/genvis.svg"))
