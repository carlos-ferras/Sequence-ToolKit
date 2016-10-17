#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from __future__ import unicode_literals
import os
import ast

from model.singlenton import Singleton


class ConfigHandler(Singleton):
    def __init__(self):
        if os.sys.platform == 'linux' or os.sys.platform == 'linux2':
            self.config_path = os.environ['HOME']+'/.sequence-toolkit/'
        else:
            try:
                self.config_path = os.environ['LOCALAPPDATA'] + '\\sequence-toolkit\\'
            except:
                self.config_path = os.environ['USERPROFILE'] + '\\sequence-toolkit\\'
        if not os.path.exists(self.config_path):
            os.mkdir(self.config_path)
            os.mkdir(os.path.join(self.config_path, 'listening'))
            os.mkdir(os.path.join(self.config_path, 'share_memory'))

        self.config_files = {
            'GLOBALS': 'stk.conf',
            'COMMON': 'common.conf',
            'STK': 'stk_app.conf',
            'GENSEC': 'gensec.conf',
            'GENREP': 'genrep.conf',
            'GENVIS': 'genvis.conf',
        }

        self.configurations = {
            'GLOBALS': {
                'lang': 'en',
                'theme': 'flatt',
                'skin': 'light',
            },
            'COMMON': {
                'font-family': 'Roboto',
                'font-size': 14,
                'font-style': 'Normal',
                'default_file_location': '',
                'opacity': 1,
            },
            'STK': {
                'pos_x': None,
                'pos_y': None,
                'width': 775,
                'height': 556,
                'running_state': 0
            },
            'GENSEC': {
                'pos_x': None,
                'pos_y': None,
                'width': 775,
                'height': 556,
                'merge_color_1': '#2196f3',
                'merge_color_2': '#3f51b5',
                'merge_color_3': '#673ab7',
                'tl': None,
                'osl': None,
                'posl': None,
                'lmosl': None,
                'esl': None,
                'pre-heat': None,
                'illumination': None,
                'irradiation': None,
                'pause': None,
                'running_state': 0
            },
            'GENREP': {
                'pos_x': None,
                'pos_y': None,
                'width': 775,
                'height': 556,
                'association_color_1': '#ffcdd2',
                'association_color_2': '#d1c4e9',
                'association_color_3': '#b2dfdb',
                'curve_to_show': [1],
                'show_tl': False,
                'horizontal_scale': 'lineal',
                'horizontal_minimun': -1,
                'horizontal_maximun': -1,
                'horizontal_greater_unit': 20,
                'horizontal_smallest_unit': 5,
                'unit': 0,
                'vertical_scale': 'lineal',
                'vertical_minimun': -1,
                'vertical_maximun': -1,
                'vertical_greater_unit': 5000,
                'vertical_smallest_unit': 500,
                'signal_active': 1,
                'low_signal': 1,
                'high_signal': 11,
                'background_active': 1,
                'low_background': -10,
                'high_background': -1,
                'consecutive': True,
                'parameters': [],
                'running_state': 0
            },
            'GENVIS': {
                'pos_x': None,
                'pos_y': None,
                'width': 775,
                'height': 556,
            },
        }

        self.load()

    def load(self):
        for config_key in self.configurations:
            path = os.path.join(self.config_path, self.config_files[config_key])
            if os.path.exists(path):
                config_file = open(path, 'r')
                content = config_file.read()

                configuration = {}
                for line in content.split('\n'):
                    if line:
                        value = line.split(' = ')[1].strip()
                        try:
                            value = ast.literal_eval(value)
                        except:
                            value = str(value)
                        configuration[line.split(' = ')[0].strip()] = value

                self.configurations[config_key] = configuration

    def save(self, config_key):
        if config_key in self.config_files:
            path = os.path.join(self.config_path, self.config_files[config_key])
            config_file = open(path, 'w+')

            for key in self.configurations[config_key]:
                config_file.write(key + ' = ' + str(self.configurations[config_key][key]) + '\n')
            config_file.close()

            return True
        else:
            raise Exception("Wrong configuration key.")

