import sys
import os
import re

variant = 'PyQt4'
#variant = 'PySide'

#print ('Python {}, {}'.format(sys.version, sys.platform))

'''
# Using PyQt4:
if variant == 'PySide':
    import PySide
    from PySide import QtGui, QtCore
    print 'PySide {}, Qt {}'.format(PySide.__version__, PySide.QtCore.__version__)
'''

# Using PySide:
if variant == 'PyQt4':
    from PyQt4 import QtGui, QtCore
    from PyQt4.Qt import PYQT_VERSION_STR
    #print ('PyQt4 {}, Qt {}'.format(PYQT_VERSION_STR, QtCore.QT_VERSION_STR))

class ExpressionValidator(QtGui.QValidator):
    ''' Useful for calculator type input
    see http://stackoverflow.com/questions/26759623/why-is-the-return-of-qtgui-qvalidator-validate-so-inconsistent-robust-way-to '''
    
    def __init__(self, parent=None,):
        QtGui.QValidator.__init__(self, parent)

        self.states = {'invalid':      QtGui.QValidator.Invalid,
                      'intermediate':  QtGui.QValidator.Intermediate,
                      'acceptable':    QtGui.QValidator.Acceptable,
                      }

        self.regX_expression = re.compile('([0-9.eEpiPI+-/*\(\))\^]*)')

    def returnState(self, state, text, pos):

        if state == 'acceptable':
            color = '#c4df9b' # green
        elif state == 'intermediate':
            color = '#fff79a' # yellow
        else:
            color = '#f6989d' # red
        self.parent().setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))

        if variant == 'PyQt4':
            return (self.states[state], text, pos)
        else:
            return (self.states[state], pos)
        '''
        if variant == 'PySide':
            return self.states[state]
        else:
            return (self.states[state], pos)
        '''

    def validate(self, textInput, pos):
        # Check text, return state
        matches = self.regX_expression.findall(textInput)
        if matches and len(matches[0]) == len(textInput):
            if len(textInput) >0 and str(textInput)[-1] in '+-/*^':
                self.parent().setToolTip('Expression incomplete')
                return self.returnState('intermediate', textInput, pos)
            else:
                return self.returnState('acceptable', textInput, pos)
        else:
            return self.returnState('invalid', textInput, pos)


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    app.setStyle('GTK')
    mainWindow = QtGui.QMainWindow()

    lineEdit = QtGui.QLineEdit()
    lineEdit.setValidator(ExpressionValidator(lineEdit))

    mainWindow.setCentralWidget(lineEdit)
    mainWindow.show()

    app.exec_()

    app.deleteLater()
    sys.exit()