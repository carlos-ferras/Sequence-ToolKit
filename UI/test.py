from PyQt4 import QtCore  
from PyQt4 import QtGui 
import axis_format
import sys

class format(axis_format.Ui_Form):
	"""Ventana para seleccionar fuente"""
	def __init__(self,parent=None):
		self.form1 =QtGui.QMainWindow(parent)
		self.setupUi(self.form1)
		self.form1.show()
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	w=format()		
	sys.exit(app.exec_())