from PyQt4.QtGui import QWidget
from gui.wellplot.subplots.ui_logplotheader import Ui_LogHeader
import logging

logger = logging.getLogger('console')

class LogPlotHeader(QWidget, Ui_LogHeader):
    '''
    simple header labels for log
    '''
    def __init__(self, parent=None):
        logger.debug(">>__init__() ")
        #QWidget.__init__(self, parent)
        super(LogPlotHeader, self).__init__(parent)
        self.setupUi(self)
