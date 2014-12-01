#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#~ Copyright (C) 2014 Carlos Manuel Ferras Hernandez
#~ This file is part of LF02_package.

#~ LF02_package is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.

#~ LF02_package is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.

#~ You should have received a copy of the GNU General Public License
#~ along with LF02_package.  If not, see <http://www.gnu.org/licenses/>.

BUTTON_STYLE="""    
QPushButton  {
	font-size:14px;
	}
"""

PROCESS_WIN_STYLE="""
QMessageBox{
	background:#FF6C6E;
}
"""

ERROR_STYLE="""
QMessageBox{
	background:#FF6C6E;
}

QMessageBox *{
	color:#FFFFFF;
	
}

QMessageBox QPushButton  {
	color:#000000;
	border-radius: 0px;
	padding: 4px 14px;
	text-align:left;
	background:qlineargradient(spread:pad, x1:0.502, y1:0.966, x2:0.462, y2:0.0397727, stop:0 rgba(223, 223, 223, 255), stop:1 rgba(255, 255, 255, 255));
}

QMessageBox QPushButton:hover  {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
}
     
QMessageBox QPushButton:pressed {
	color:#ffffff;
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
}
"""

BUTTON_OPTION_STYLE="""    
QPushButton  {
	border-radius: 0px;
	padding: 4px 14px;
	text-align:left;
	font-size:14px;
	background:qlineargradient(spread:pad, x1:0.502, y1:0.966, x2:0.462, y2:0.0397727, stop:0 rgba(223, 223, 223, 255), stop:1 rgba(255, 255, 255, 255));
}

QPushButton:hover  {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
}
     
QPushButton:pressed {
	color:#ffffff;
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
}

"""


TREEW_STYLE="""
QTreeWidget{show-decoration-selected: 1;}

QTreeWidget::item {
	border: 1px solid #d9d9d9;
	border-top-color: transparent;
}

QTreeWidget::item:hover {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
	border: 1px solid #bfcde4;
}

QTreeWidget::item:selected {
	border: 1px solid #567dbc;
}

QTreeWidget::item:selected:active{
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}

QTreeWidget::item:selected:!active {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
}
"""


TREEW2_STYLE="""
QTreeWidget::item {
}

QTreeWidget::item:hover {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
	border: 1px solid #bfcde4;
}

QTreeWidget::item:selected {
	border: 1px solid #567dbc;
}

QTreeWidget::item:selected:active{
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}

QTreeWidget::item:selected:!active {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
}
"""

HEADER_TOOLBUTTON_STYLE="""
QToolButton{
	border-radius: 0px;
	font:16px;
	background:qlineargradient(spread:pad, x1:0.502, y1:0.966, x2:0.462, y2:0.0397727, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(240, 240, 240, 255))
}

QToolButton:hover {
	background:#FFFFFF;
}

QToolButton:!enabled  {
	color:#000000;
}

"""

HEADER_TOOLBUTTON_STYLE2="""
QToolButton{
	border-radius: 0px;
	font:16px;
	background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}

QToolButton:hover {
	background:#FFFFFF;
}

QToolButton:!enabled  {
	color:#000000;
}

"""


HEADER="""
QHeaderView::section{
	border-radius: 0px;
	padding:3px;
	font:16px;
	background:qlineargradient(spread:pad, x1:0.502, y1:0.966, x2:0.462, y2:0.0397727, stop:0 rgba(220, 220, 220, 255), stop:1 rgba(240, 240, 240, 255))
}

QHeaderView::section:hover {
	background:#FFFFFF;
}

"""


TOOLBUTTON_STYLE="""  
QToolButton  {
	border-radius: 0px;
	margin-right:10px;
	margin-top:3px;
	margin-bottom:2px;
}

QToolButton:hover  {
	border: 2px solid #567dbc;
}
     
QToolButton:pressed  {
	border: 2px solid #cbdaf1;
}

"""

MENU_STYLE="""
QMenuBar {
	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}

QMenuBar::item {
	padding: 4px 4px;
	background: transparent;
	color:#ffffff;
}

QMenuBar::item:selected {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
	color: #567dbc;
}

QMenuBar::item:pressed {
	background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
	color: #567dbc;
}

QMenu {
	background-color: #cbdaf1;
	color: #567dbc;
}

QMenu::item {
	background-color: transparent;
}

QMenu::item:selected {
	color:#ffffff;
	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}
 """
 
 
TOOLBAR_STYLE="""
background: red;
 """

