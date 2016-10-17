#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import os
from datetime import datetime
from PyQt5 import QtCore, QtNetwork

from model.singlenton import Singleton


class BaseSignals(QtCore.QObject):
    recent_file_added = QtCore.pyqtSignal()


class RecentFilesHandler(Singleton):
    def __init__(self):
        self.signals = BaseSignals()

        if os.sys.platform == 'linux' or os.sys.platform == 'linux2':
            config_path = os.environ['HOME'] + '/.sequence-toolkit/'
        else:
            try:
                config_path = os.environ['LOCALAPPDATA'] + '\\sequence-toolkit\\'
            except:
                config_path = os.environ['USERPROFILE'] + '\\sequence-toolkit\\'
        if not os.path.exists(config_path):
            os.mkdir(config_path)

        self.recent_files_path = os.path.join(config_path, 'recent_files')

        self.recent_files = {
            'GENSEC': [],
            'GENREP': [],
            'GENVIS': [],
        }

        self.load()

    def appendPath(self, path, app_name):
        if app_name in self.recent_files:
            self.recent_files[app_name] = list(
                filter(
                    lambda date_path: date_path[1] != path,
                    self.recent_files[app_name]
                )
            )
            self.recent_files[app_name].insert(0, [str(datetime.now()), path])
            self.recent_files[app_name] = self.recent_files[app_name][:10]

            self.save()

    def getGlobal(self):
        recent_files = []

        for app_name in self.recent_files:
            for date_path in self.recent_files[app_name]:
                if os.path.exists(date_path[1]):
                    date = datetime.strptime(date_path[0], "%Y-%m-%d %H:%M:%S.%f")
                    added = False
                    for i in range(len(recent_files)):
                        date_2 = datetime.strptime(recent_files[i][0], "%Y-%m-%d %H:%M:%S.%f")
                        if date > date_2:
                            recent_files.insert(i, date_path)
                            added = True
                            break
                    if not added:
                        recent_files.append(date_path)

        cleaned = []
        for file in recent_files:
            add = True
            for clean_file in cleaned:
                if file[1] == clean_file[1]:
                    add = False
                    break
            if add:
                cleaned.append(file)

        return cleaned

    def load(self):
        if os.path.exists(self.recent_files_path):
            config_file = open(self.recent_files_path, 'r')
            content = config_file.read()

            app_name = None
            for line in content.split('\n'):
                if line:
                    if line.strip() in self.recent_files:
                        app_name = line.strip()
                    elif app_name is not None:
                        date = line.split(']')[0].strip().split('[')[-1].strip()
                        path = line.split(']')[-1].strip()

                        if os.path.exists(path) and os.path.isfile(path):
                            self.recent_files[app_name].append([date, path])

    def save(self):
        config_file = open(self.recent_files_path, 'w+')
        for app_name in self.recent_files:
            config_file.write(app_name + '\n')
            for date_path in self.recent_files[app_name]:
                config_file.write('[' + date_path[0] + '] ' + date_path[1] + '\n')
            config_file.write('\n\n')

        self.signals.recent_file_added.emit()