#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import os
import sys

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(base_dir)

from model.handle_app import AppHandler
from controller.genrep.genrep import GenRep


if __name__ == "__main__":
    app = AppHandler('GENREP', sys.argv)

    if app.is_running:
        app.sendMessage(sys.argv[1:])
    else:
        app.start(GenRep)
        sys.exit(app.exec_())
