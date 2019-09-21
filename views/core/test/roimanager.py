from PyQt4 import QtCore as QC

from views.core.test.senderobject import SenderObject

import logging

logger = logging.getLogger(__name__)


class ROIManager(QC.QObject):
    #equivalent to WellPlot
    
    def __init__(self, parent=None):
        super(ROIManager,self).__init__(parent)
        self.sender = SenderObject()
        
    def add_snaproi(self):
        logger.debug(">>add_snaproi()")
        self.sender.something_happened.connect(self.new_roi)
        
    def new_roi(self):
        logger.debug('>>new_roi() Something happened in ROI!')