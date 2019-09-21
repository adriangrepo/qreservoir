from PyQt4 import QtCore, QtGui
from globalvalues.constants.dataitemconstants import DataItemConstants
from globalvalues.constants.colorconstants import ColorConstants


class RealValidator(QtGui.QDoubleValidator):
    ''' Evaluates text (eg in QLineEdit) and checks if is number or None '''
    
    '''
    def validate(self, value, pos):
        text = value.strip().title()
        #for null in ('None', 'Null', 'Nothing'):
        for null in (DataItemConstants.DB_NULL):
            if text == null:
                return QtGui.QValidator.Acceptable, text, pos
            if null.startswith(text):
                return QtGui.QValidator.Intermediate, text, pos
        return super(RealValidator, self).validate(value, pos)
    '''
    
    def validate(self, value, pos):
        text = value.strip().title()
        if text == DataItemConstants.DB_NULL:
            return QtGui.QValidator.Acceptable, text, pos
        if DataItemConstants.DB_NULL.startswith(text):
            return QtGui.QValidator.Intermediate, text, pos
        return super(RealValidator, self).validate(value, pos)

    
    

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.edit = QtGui.QLineEdit(self)
        self.edit.setValidator(RealValidator(self.edit))
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.edit)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 200, 50)
    window.show()
    sys.exit(app.exec_())