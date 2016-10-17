#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import pickle

from PyQt5 import QtWidgets, QtCore, QtNetwork


class Assistant(QtWidgets.QApplication):
    timeout = 1000

    def __init__(self, argv):
        QtWidgets.QApplication.__init__(self, argv)

        self.socket_filename = os.path.expanduser("~/.stk_assistant_share_memory")
        self.shared_memory = QtCore.QSharedMemory()
        self.shared_memory.setKey(self.socket_filename)

        self.is_running = self.shared_memory.attach()
        self.process = None

        if not self.is_running:
            if not self.shared_memory.create(1):
                return
            self.process = QtCore.QProcess()
            self.process.finished.connect(self.quit)

            self.server = QtNetwork.QLocalServer(self)
            self.server.newConnection.connect(self.receiveMessage)
            self.server.listen(self.socket_filename)

    def start(self):
        if not self.process:
            self.process = QtCore.QProcess()
        if self.process.state() != QtCore.QProcess.Running:
            app = "assistant "
            args = "-collectionFile resources/help/stk_collection.qhc -enableRemoteControl"
            self.process.start(app + args)

            if len(self.arguments()) == 2 and \
                    self.arguments()[1] in ['stk', 'gensec', 'genrep', 'genvis']:
                self.handleMessage(self.arguments()[1])
        return True

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

    def handleMessage(self, content):
        msg = QtCore.QByteArray()
        msg.append('show index;')
        msg.append('activateKeyword ' + content + ';')
        msg.append('setSource ' + 'qthelp://com.sequence-toolkit.help-assistant/doc/html/' + content + '.html\n')
        self.process.write(msg)

    def quit(self):
        self.shared_memory.detach()
        os.remove(self.socket_filename)

        if self.process is not None:
            if self.process.state() == QtCore.QProcess.Running:
                self.process.terminate()
                self.process.waitForFinished(3000)
            self.process.deleteLater()
        QtWidgets.QApplication.quit()
