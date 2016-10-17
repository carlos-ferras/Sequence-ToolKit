#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from functools import partial

from PyQt5 import QtGui, QtCore

from controller.gensec.dialogs.processes.esl import ESL
from controller.gensec.dialogs.processes.illumination import Illumination
from controller.gensec.dialogs.processes.irradiation import Irradiation
from controller.gensec.dialogs.processes.lmosl import LMOSL
from controller.gensec.dialogs.processes.osl import OSL
from controller.gensec.dialogs.processes.pause import Pause
from controller.gensec.dialogs.processes.posl import POSL
from controller.gensec.dialogs.processes.pre_heat import PreHeat
from controller.gensec.dialogs.processes.tl import TL
from model.handle_config import ConfigHandler
from view.dialogs.base_dialog import BaseDialog
from view.gensec.dialogs.ui_processes_set import Ui_processes


class ProcessesSet(BaseDialog, Ui_processes):
    process_accepted = QtCore.pyqtSignal(tuple, tuple)

    def __init__(self, cell_position, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.process_dialog = None

        self.config_handler = ConfigHandler()
        self.cell_position = cell_position

        self.push_button_tl.clicked.connect(partial(self.getProcessDialog, 'TL'))
        self.push_button_osl.clicked.connect(partial(self.getProcessDialog, 'OSL'))
        self.push_button_posl.clicked.connect(partial(self.getProcessDialog, 'POSL'))
        self.push_button_lmosl.clicked.connect(partial(self.getProcessDialog, 'LMOSL'))
        self.push_button_esl.clicked.connect(partial(self.getProcessDialog, 'ESL'))
        self.push_button_pre_heat.clicked.connect(partial(self.getProcessDialog, 'Pre-Heat'))
        self.push_button_illumination.clicked.connect(partial(self.getProcessDialog, 'Illumination'))
        self.push_button_irradiation.clicked.connect(partial(self.getProcessDialog, 'Irradiation'))
        self.push_button_pause.clicked.connect(partial(self.getProcessDialog, 'Pause'))

        cursor_position = QtGui.QCursor.pos()
        x = cursor_position.x()
        y = cursor_position.y()
        self.setGeometry(QtCore.QRect(x + 5, y + 5, 157, 287))

        self.push_button_esl.setHidden(True)

    def getProcessDialog(self, process_name, process_data=False):
        self.setHidden(True)
        self.process_dialog = self.processFactory(process_name, process_data)
        self.process_dialog.accepted.connect(partial(self.processAccepted, process_name))
        self.process_dialog.exec_()
        self.process_dialog.deleteLater()
        self.close()

    def processAccepted(self, process_name):
        data, all_ = self.process_dialog.getData()
        self.setConfiguration(process_name.lower().split()[-1], all_)
        all_['process_order_id'] = self.cell_position[1] - 1
        all_['status'] = 'pend'
        all_['curve1'] = ''
        all_['curve2'] = ''
        all_['curve3'] = ''
        all_['time1'] = ''
        all_['time2'] = ''
        self.process_accepted.emit((data, all_), self.cell_position)
        return

    def processFactory(self, process_name, process_data=False):
        if not process_data:
            process_data = self.getConfiguration(process_name.lower())

        factory = {
            'TL': TL,
            'OSL': OSL,
            'POSL': POSL,
            'LMOSL': LMOSL,
            'ESL': ESL,
            'Pre-Heat': PreHeat,
            'Illumination': Illumination,
            'Irradiation': Irradiation,
            'Pause': Pause,
        }

        return factory[process_name](process_data, self)

    def getConfiguration(self, key, file='GENSEC'):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file='GENSEC'):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
