#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import webbrowser

from view.dialogs.base_dialog import BaseDialog
from view.dialogs.about.ui_about import Ui_about
from controller.dialogs.about.credits import Credits
from controller.dialogs.about.license import License


class About(BaseDialog, Ui_about):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.push_button_license.clicked.connect(self.license)
        self.push_button_contact.clicked.connect(self.contact)
        self.push_button_credits.clicked.connect(self.credits)

    def license(self):
        self.verticalLayout.removeWidget(self.widget)
        self.widget.deleteLater()
        self.widget = License(self)
        self.verticalLayout.insertWidget(0, self.widget)
        self.sizeIncrement()

    def credits(self):
        self.verticalLayout.removeWidget(self.widget)
        self.widget.deleteLater()
        self.widget = Credits(self)
        self.verticalLayout.insertWidget(0, self.widget)
        self.sizeIncrement()

    def contact(self):
        webbrowser.open('mailto:ceaden@ceaden.edu.cu')
