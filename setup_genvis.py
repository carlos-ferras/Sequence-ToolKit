#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from distutils.core import setup
import os
import sys
import py2exe


base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(base_dir)

includes = [
    "sip",
    "PyQt5",
    "PyQt5.QtCore",
    "PyQt5.QtGui",
    "PyQt5.QtWidgets",
    "PyQt5.QtPrintSupport",
    "PyQt5.QtNetwork",
    "PyQt5.QtXml",
    "PyQt5.QtSvg",
]

datafiles = [
    ("platforms", ["C:\\Users\\tester-vm\\Desktop\\WinPython-32bit-3.4.4.4Qt5\\python-3.4.4\\Lib\\site-packages\\PyQt5\\plugins\\platforms\\qwindows.dll"]),
    ("imageformats", ["C:\\Users\\tester-vm\\Desktop\\WinPython-32bit-3.4.4.4Qt5\\python-3.4.4\\Lib\\site-packages\\PyQt5\\plugins\\imageformats\\qico.dll"]),
    ("imageformats", ["C:\\Users\\tester-vm\\Desktop\\WinPython-32bit-3.4.4.4Qt5\\python-3.4.4\\Lib\\site-packages\\PyQt5\\plugins\\imageformats\\qsvg.dll"]),
    ("imageformats", ["C:\\Users\\tester-vm\\Desktop\\WinPython-32bit-3.4.4.4Qt5\\python-3.4.4\\Lib\\site-packages\\PyQt5\\plugins\\imageformats\\qjpeg.dll"]),
    ("iconengines", ["C:\\Users\\tester-vm\\Desktop\\WinPython-32bit-3.4.4.4Qt5\\python-3.4.4\\Lib\\site-packages\\PyQt5\\plugins\\iconengines\\qsvgicon.dll"]),
]

setup(
    name='GenVis',
    version='1.0.1',
    url='',
    license='GPL v3',
    author='Carlos Manuel Ferrás Hernández',
    author_email='c4rlos.ferra5@gmail.com',
    data_files=datafiles,
    windows=[{
        'script': 'genvis.py',
        'description': 'Repor Analyzer',
        'icon_resources': [(0, 'resources/img/logos/genvis.ico')],
        'dest_base': 'GenVis'
    }],
    zipfile=None,
    options={
        "py2exe":{
            "includes": includes,
            'bundle_files': 3,
            'compressed': True,
            'optimize': 2
        }
    }
)
