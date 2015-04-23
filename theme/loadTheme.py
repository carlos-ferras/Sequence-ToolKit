#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#~ Copyright (C) 2014 Carlos Manuel Ferras Hernandez <c4rlos.ferra5@gmail.com>
#~ This file is part of Sequence-ToolKit.

#~ Sequence-ToolKit is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.

#~ Sequence-ToolKit is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.

#~ You should have received a copy of the GNU General Public License
#~ along with Sequence-ToolKit.  If not, see <http://www.gnu.org/licenses/>.

import os

def LOAD(theme):
	colors=[]
	if os.path.exists('theme/'+theme+'.stkthm'):
		theme_values=open('theme/'+theme+'.stkthm')
		lines=theme_values.readlines()		
		for i in range(len(lines)):
			colors.append(str(lines[i].split(' ')[1][:-1]))
	elif len(colors)!=8:
		colors=['#F5F5F5','#FFFFFF','#F0F0F0','#E8E8E8','#222020','#DEDEDE','#E3E3E3','#000000']
	return colors
	
	

