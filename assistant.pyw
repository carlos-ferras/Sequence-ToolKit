#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import sys

base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(base_dir)

from controller.stk.assistant import Assistant

if __name__ == "__main__":
    app = Assistant(sys.argv)

    if app.is_running:
        if len(sys.argv) == 2 and \
                    sys.argv[1] in ['stk', 'gensec', 'genrep', 'genvis']:
            app.sendMessage(sys.argv[1])
    else:
        app.start()
        sys.exit(app.exec_())
