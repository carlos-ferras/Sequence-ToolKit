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

def BASE(COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8,usar=False):

	first= """
	*{
		font-size:14px;
		}

	QDialog,QMainWindow,QFileDialog,QWidget{
		background: %s;
		color:%s;
	}
	"""%(COL1,COL8)
	
	if usar:
		middle="""
		QTreeWidget{
			show-decoration-selected: 1;
			background: %s;			
		}

		QTreeWidget::item {
			border-top-color: transparent;
			background: %s;			
		}

		QTreeWidget::item:alternate {
		     background: %s;
		 }
		 """%(COL2,COL2,COL3)
	else:		
		middle="""
		QTreeWidget{
			show-decoration-selected: 1;
		}

		QTreeWidget::item {
			border-top-color: transparent;
		}

		QTreeWidget::item:alternate {
		 }
		 """
	 
	second="""
	QTreeWidget::item:hover {
		background: %s;
	}

	QTreeWidget::item:selected:active{
		background: %s;
		color: %s;
	}

	QTreeWidget::item:selected:!active {
		background: %s;
		color: %s;
	}

	QHeaderView::section 
	{
		background: %s;
		color: %s;
		font:16px;
		padding: 4px;
		border: 0px;
	}

	QHeaderView::section:hover{
		background:%s;
	}

	QTreeWidget QToolButton{
		background: %s;
		color: %s;
		font:16px;
		border: 0px;	
	}

	QTreeWidget QToolButton:hover {
		background:%s;
	}

	QTreeWidget QToolButton:!enabled  {
		color:%s;
	}

	QMenuBar {
		background-color: %s;
	}

	QMenuBar::item {
		padding: 4px 4px;
		background: transparent;
		color:%s;
	}

	QMenuBar::item:selected {
		background: %s;
	}

	QMenuBar::item:pressed {
		background: %s;
	}

	QMenu {
		background-color:%s;
		color: %s;
	}

	QMenu::item {
		background-color: transparent;
	}

	QMenu::item:selected {
		background-color: %s;
	}

	QToolBar{
		background-color: %s;
		border: 1px solid %s;
	}

	QToolBar::handle {
	     image: url(handle.png);
	 }

	QPushButton  {
		border-radius: 0px;
		padding: 4px 14px;
		text-align:left;
		background:%s;
	}

	QPushButton:hover  {
		background: %s;
	}
	     
	QPushButton:pressed {
		background: %s;
	}

	QToolButton  {
		background-color: %s;
		border-radius: 0px;
		margin-right:10px;
		margin-top:3px;
		margin-bottom:2px;
	}

	QToolButton:hover  {
		border: 3px solid %s;
	}
	     
	QToolButton:pressed  {
		border: 4px solid %s;
	}

	QTextEdit{
		background:%s;
		font:16px;
	}

	QComboBox {
		border-radius: 0px;
		background: %s;		
	 }

	 QComboBox:editable {
		background: %s;		
	 }

	 QComboBox::drop-down {
		subcontrol-origin: padding;
		subcontrol-position: top right;

		border-left-width: 1px;
		border-left-color: %s;
		border-left-style: solid;
		border-radius: 0px;
	 }

	 QComboBox::down-arrow {
		image: url(pixmaps/icons/down.png);
	 }

	 QComboBox::down-arrow:on {
		top: 1px;
		left: 1px;
	 }
	 
	 QComboBox QAbstractItemView {
		background:%s;
		selection-background-color: %s;
		color:%s;
		selection-color:%s;
		border-radius: 0px;
	 }
	 
	 QSpinBox,QDoubleSpinBox {
	     padding-right: 15px; 
	     background: %s;
	     border-radius: 0px;
	 }

	 QSpinBox::up-arrow ,QDoubleSpinBox::up-arrow {
	     image: url(pixmaps/icons/up.png)
	 }

	 QSpinBox::down-arrow ,QDoubleSpinBox::down-arrow{
	    image: url(pixmaps/icons/down.png)
	 }

	QCheckBox {
	     spacing: 5px;
	 }

	 QListWidget::indicator:unchecked,QCheckBox::indicator:unchecked {
	     image: url(pixmaps/icons/checkbox_unchecked.png)
	 }

	 QListWidget::indicator:unchecked:hover, QCheckBox::indicator:unchecked:hover {
	     image: url(pixmaps/icons/checkbox_unchecked_hover.png)
	 }

	 QListWidget::indicator:unchecked:pressed , QCheckBox::indicator:unchecked:pressed {
	     image: url(pixmaps/icons/checkbox_unchecked.png)
	 }

	 QListWidget::indicator:checked , QCheckBox::indicator:checked {
	     image: url(pixmaps/icons/checkbox_checked.png)
	 }

	 QListWidget::indicator:checked:hover , QCheckBox::indicator:checked:hover {
	     image: url(pixmaps/icons/checkbox_checked_hover.png)
	 }

	 QListWidget::indicator:checked:pressed , QCheckBox::indicator:checked:pressed {
	     image: url(pixmaps/icons/checkbox_checked.png)
	 }

	QRadioButton {
	     spacing: 5px;
	 }

	 QRadioButton::indicator::unchecked {
	     image: url(pixmaps/icons/radiobutton_unchecked.png)
	 }

	 QRadioButton::indicator:unchecked:hover {
	     image: url(pixmaps/icons/radiobutton_unchecked_hover.png)
	 }

	 QRadioButton::indicator:unchecked:pressed {
	     image: url(pixmaps/icons/radiobutton_unchecked.png)
	 }

	 QRadioButton::indicator::checked {
	     image: url(pixmaps/icons/radiobutton_checked.png)
	 }

	 QRadioButton::indicator:checked:hover {
	     image: url(pixmaps/icons/radiobutton_checked_hover.png)
	 }

	 QRadioButton::indicator:checked:pressed {
	     image: url(pixmaps/icons/radiobutton_checked.png)
	 }
	 
	 QLineEdit{
		border-radius: 0px;
		background:%s;
	 }
	 
	 QTabWidget::tab-bar {
		left: 5px;
	 }
	 
	 QTabBar::tab {
		background: %s;
		border: 2px solid %s;
		border-bottom-color: %s; 
		border-radius: 0px;
		min-width: 8ex;
		padding: 2px;
	 }

	 QTabBar::tab:selected, QTabBar::tab:hover {
		background: %s;
	 }
	"""%(COL1,COL4,COL5,COL4,COL5,COL1,COL8,COL2,COL1,COL8,COL2,COL8,COL6,COL8,COL2,COL2,COL2,COL8,COL6,COL7,COL7,COL2,COL1,COL4,COL7,COL7,COL7,COL2,COL2,COL2,COL6,COL2,COL1,COL8,COL8,COL2,COL2,COL2,COL1,COL1,COL1)

	
	return first+middle+second