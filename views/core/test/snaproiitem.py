
from views.core.test.senderobject import SenderObject
from PyQt4 import QtGui as QG
import logging

logger = logging.getLogger(__name__)

class SnapROIItem(QG.QGraphicsItem):
    #equivalent to LayoutDialog
    
    def __init__(self, parent = None):
        super(SnapROIItem, self).__init__(parent)
        self.sender = SenderObject()
        
    def do_something_and_emit(self):
        logger.debug(">>do_something_and_emit()")
        self.sender.something_happened.emit()