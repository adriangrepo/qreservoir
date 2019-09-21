from PyQt4.QtGui import QToolBar
from PyQt4 import QtGui, QtCore 
from PyQt4.QtCore import QObject
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#http://article.gmane.org/gmane.comp.python.pyqt-pykde/9245
_oldConnect = QtCore.QObject.connect
_oldDisconnect = QtCore.QObject.disconnect
_oldEmit = QtCore.QObject.emit

def _wrapConnect(callableObject):
    """Returns a wrapped call to the old version of QtCore.QObject.connect"""
    
    logger.debug(">>_wrapConnect()")
    
    @staticmethod
    def call(*args):
        logger.debug(">>call()")
        callableObject(*args)
        _oldConnect(*args)
    return call

def _wrapDisconnect(callableObject):
    """Returns a wrapped call to the old version of QtCore.QObject.disconnect"""
    
    logger.debug(">>_wrapDisconnect()")
    
    @staticmethod
    def call(*args):
        logger.debug(">>call()")
        callableObject(*args)
        _oldDisconnect(*args)
    return call

def enableSignalDebugging(**kwargs):
    """Call this to enable Qt Signal debugging. This will trap all
    connect, and disconnect calls."""
    
    logger.debug(">>enableSignalDebugging()")
    
    f = lambda *args: None
    connectCall = kwargs.get('connectCall', f)
    disconnectCall = kwargs.get('disconnectCall', f)
    emitCall = kwargs.get('emitCall', f)

    def printIt(msg):
        logger.debug(">>printIt()")
        def call(*args):
            print ("--printIt() "+msg, args)
        return call
    QtCore.QObject.connect = _wrapConnect(connectCall)
    QtCore.QObject.disconnect = _wrapDisconnect(disconnectCall)

    def new_emit(self, *args):
        logger.debug(">>new_emit()")
        emitCall(self, *args)
        _oldEmit(self, *args)

    QtCore.QObject.emit = new_emit