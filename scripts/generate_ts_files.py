#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-


import os


base_command = 'pylupdate5 -noobsolete -verbose {0}-ts {1}'

ts_files = [
	{
		'dest' : '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/i18n/ts/i18n_stk.ts',
		'folders': [
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/dialogs',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/dialogs/about',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/stk',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/stk/dialogs',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/widgets',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/dialogs',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/dialogs/about',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/widgets',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/stk',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/stk/dialogs',
		],
		'files': ''
	},
	{
		'dest' : '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/i18n/ts/i18n_gensec.ts',
		'folders': [
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/gensec',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/gensec/dialogs',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/gensec/dialogs/processes',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/gensec',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/gensec/dialogs',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/gensec/dialogs/processes',
		],
		'files': ''
	},
	{
		'dest' : '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/i18n/ts/i18n_genrep.ts',
		'folders': [
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/genrep',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/genrep/dialogs',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/genrep',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/genrep/dialogs',
		],
		'files': ''
	},
	{
		'dest' : '/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/resources/i18n/ts/i18n_genvis.ts',
		'folders': [
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/genvis',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/controller/genvis/dialogs',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/genvis',
			'/home/krl1to5/Work/FULL/Sequence-ToolKit/2016/view/genvis/dialogs',
		],
		'files': ''
	},
]

for i in range(len(ts_files)):
	for folder in ts_files[i]['folders']:
		for path,j,k in os.walk(folder):
			if k:
				for file_name in k:
					if file_name.endswith('.py'):
						ts_files[i]['files'] += os.path.join(path, file_name) + ' '
	os.system(base_command.format(ts_files[i]['files'], ts_files[i]['dest']))