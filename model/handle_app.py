#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from __future__ import unicode_literals
import os
import sys
import pickle
from PyQt5 import QtCore, QtWidgets, QtNetwork

from model.handle_config import ConfigHandler


class AppHandler(QtWidgets.QApplication): 
    timeout = 1000

    def __init__(self, appname, argv):
        QtWidgets.QApplication.__init__(self, argv)
        self.appname = appname
        self.windows = None

        self.config_handler = ConfigHandler()

        self.socket_filename = os.path.join(self.config_handler.config_path, 'share_memory', appname)
        self.shared_memory = QtCore.QSharedMemory()
        self.shared_memory.setKey(self.socket_filename)

        self.is_running = self.shared_memory.attach()
        if self.is_running and self.getConfiguration('running_state') == 0:
            self.shared_memory.detach()
            self.is_running = self.shared_memory.attach()
        self.setConfiguration('running_state', 1)

        if not self.is_running:
            if not self.shared_memory.create(1):
                return
            self.server = QtNetwork.QLocalServer(self)
            self.server.newConnection.connect(self.receiveMessage)
            self.server.listen(self.socket_filename)

    def __del__(self):
        self.shared_memory.detach()

    def sendMessage(self, message):
        if not self.is_running:
            raise Exception("Client cannot connect to the server. Not running.")
        socket = QtNetwork.QLocalSocket(self)
        socket.connectToServer(self.socket_filename, QtCore.QIODevice.WriteOnly)
        if not socket.waitForConnected(self.timeout):
            raise Exception(str(socket.errorString()))
        socket.write(pickle.dumps(message))
        if not socket.waitForBytesWritten(self.timeout):
            raise Exception(str(socket.errorString()))
        socket.disconnectFromServer()

    def receiveMessage(self):
        socket = self.server.nextPendingConnection()
        if not socket.waitForReadyRead(self.timeout):
            return
        byte_array = socket.readAll()
        self.handleMessage(pickle.loads(byte_array))

    def handleMessage(self, message):
        self.windows.openSLF(message)
        self.windows.main_window.activateWindow()

    def start(self, app):
        self.windows = app(self.appname, dirs=sys.argv[1:])
        self.windows.main_window.showMaximized()

    def getConfiguration(self, key):
        return self.config_handler.configurations[self.appname][key]

    def setConfiguration(self, key, value):
        self.config_handler.configurations[self.appname][key] = value
        self.config_handler.save(self.appname)
