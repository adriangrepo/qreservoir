import sys
import os
import logging
from PyQt4 import QtGui

logger = logging.getLogger('console')

class Notepad(QtGui.QDialog):

    def __init__(self, parent, filename):
        super(Notepad, self).__init__(parent)
        self.filename = filename
        self.initUI() 
        self.showFile()
        
    def initUI(self):

        hbox = QtGui.QHBoxLayout()
        self.text = QtGui.QTextEdit(self)
        hbox.addWidget(self.text)
        self.setGeometry(600,600,600,600)
        self.setWindowTitle(str(self.filename))
        self.setLayout(hbox)

    def showFile(self):
        try:
            f = open(self.filename, 'r')
            filedata = f.read()
            self.text.setText(filedata)
            f.close()      
        except IOError:
            logger.error("Cannot open file "+str(filename))  
        

       