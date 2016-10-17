#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from view.dialogs.base_dialog import BaseDialog
from view.stk.dialogs.ui_open_with import Ui_open_with


class OpenWith(BaseDialog, Ui_open_with):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.push_button_gensec.clicked.connect(self.accept)
        self.push_button_genrep.clicked.connect(self.accept)
