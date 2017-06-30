Sequence-ToolKit
======

Is used in the generation and posterior analysis of the measurement sequences. 
The STK was programmed on the basis of technical task elaborated by the LF02 developers. 

For the accomplishment of these tasks the
STK has a set of applications (GenSec, GenRep, GenVis) and a help assistant .

This package is the result of the collaboration between the department of free software from the University of Informatics Sciences (UCI)
in Havana and the Luminescence Dating Laboratory at CEADEN.

Created and Designed by: Carlos Manuel Ferr�s Hern�ndez

Documented by: Yanet Leonor Quesada Hern�ndez

XML structure and concepts: Luis Baly Gil

http://www.uci.cu
http://www.ceaden.cu/
======

Generate .py file from .ui
pyuic5 input.ui -o output.py

Generate .ts file from .py
pylupdate5 -verbose *.py -ts traslator_file.ts

Generate .py resource file from .qrc resource
pyrcc5 -o images_rc.py images.qrc

Generate .qhc file from .qhcf
qcollectiongenerator stk_collection.qhcp -o stk_collection.qhc

PyQt5 examples directory
/usr/share/doc/pyqt5-examples/examples
