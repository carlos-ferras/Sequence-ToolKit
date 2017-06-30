#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import os
import sys

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(base_dir)

from model.handle_app import AppHandler
from controller.gensec.gensec import GenSec


if __name__ == "__main__":
    app = AppHandler('GENSEC', sys.argv)

    if app.is_running:
        app.sendMessage(sys.argv[1:])
    else:
        app.start(GenSec)
        sys.exit(app.exec_())
