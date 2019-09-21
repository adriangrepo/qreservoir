from __future__ import unicode_literals

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import (Qt, pyqtSignal, QObject, QEvent)
from PyQt4.QtGui import (QComboBox, QDialog,  QTableWidgetItem, QTableWidget, QWizardPage, QWizard, QMessageBox, QWidget)
#import lasio.pylasdev.las_reader
import logging
import totaldepth.PlotLogs
import inout.las.reader.ui.logtablemodel as logtablemodel

from db.core.well.well import Well
from inout.las.reader.ui.wizard.ui_welllaswizardpage import Ui_WellLasWizardPage
from inout.las.reader.lasreader import LasReader
from inout.las.reader.ui.notepad import Notepad
from statics.types.logtype import LogType
from statics.types.logunitstype import LogUnitsType
from statics.types.zaxis import ZAxis
from statics.types.referenceleveltype import ReferenceLevelType
from globalvalues.constants.colorconstants import ColorConstants
from inout.validation.realvalidator import RealValidator
from qrutilities.numberutils import NumberUtils
from db.core.well.welldao import WellDao


logger = logging.getLogger('console')

class WellLasWizardPage(QWizardPage, Ui_WellLasWizardPage):
    '''
    Well data, plus option to import required or all data
    '''
    
    def __init__(self, well, parent=None):
        logger.debug(">>__init__() ")
        assert well is not None
        super(WellLasWizardPage, self).__init__(parent)
        self._well = well
        self._completeChanged = pyqtSignal()
        #store parent QWizard as parent type changes to QForm after __init__
        self._parent = parent
        #Only relevant if importing to existing well 
        self._overwiteExistingData = False
        self.setupUi(self)
        self.setExistingWellNames()
        self.populateWidgets()
        self.populateComboBoxes()
        self.setComboInitialStates()
        self.connectSlots()
        self.setValidators()
        self.attachNonRequiredCheckers()
        self.attachRequiredCheckers()
        self.setDefaultState()
 
    #Populate data
    
    def setExistingWellNames(self):
        ''' Check existing Well names in database and populate combobox '''
        logger.debug("setExistingWellNames() "+ str(self.wizard()))

        if self._parent._wellExistsInDB:
            session = self._parent._session
            wells = WellDao.getAllWells(session)
            for well in wells:
                self.existingWellComboBox.addItem(well.name)
    
    def populateWidgets(self):
          
        self.wellNameLineEdit.setText(self._well.name)
        
        if self._well.elevation_of_depth_reference is None: 
            self.elevationOfDepthReferenceLineEdit.setText("")
        else:
            self.elevationOfDepthReferenceLineEdit.setText(str(self._well.elevation_of_depth_reference))
                
        self.areaLineEdit.setText(self._well.area)
        self.apiLineEdit.setText(self._well.api)
        self.blockLineEdit.setText(self._well.block)
        self.companyLineEdit.setText(self._well.company)
        self.completionStatusLineEdit.setText(self._well.completion_status)
        self.countryLineEdit.setText(self._well.country)
        self.countyLineEdit.setText(self._well.county)
        self.fieldLineEdit.setText(self._well.field)
        self.licenseLineEdit.setText(self._well.license)
        self.locationLineEdit.setText(self._well.location)
        self.operatorLineEdit.setText(self._well.operator)
        self.provinceLineEdit.setText(self._well.province)
        self.stateLineEdit.setText(self._well.state)
        self.uwiLineEdit.setText(self._well.uwi)
        self.drillingContractorLineEdit.setText(self._well.drilling_contractor)
        self.rigNameLineEdit.setText(self._well.rig_name)
        self.spudDateLineEdit.setText(self._well.spud_date)
        self.tdDateLineEdit.setText(self._well.td_date)
        
        if self._well.td_driller is None: 
            self.tdDrillerLineEdit.setText("")
        else:
            self.tdDrillerLineEdit.setText(str(self._well.td_driller))
        if self._well.water_depth is None: 
            self.waterDepthLineEdit.setText("")   
        else:
            self.waterDepthLineEdit.setText(str(self._well.water_depth))             
        if self._well.df_elevation is None: 
            self.dfElevationLineEdit.setText("")   
        else:
            self.dfElevationLineEdit.setText(str(self._well.df_elevation))  
        if self._well.kb_elevation is None: 
            self.kbElevationLineEdit.setText("")   
        else:
            self.kbElevationLineEdit.setText(str(self._well.kb_elevation))        
        if self._well.gl_elevation is None: 
            self.glElevationLineEdit.setText("")   
        else:
            self.glElevationLineEdit.setText(str(self._well.gl_elevation))     
     
        self.geodeticDatumLineEdit.setText(self._well.geodetic_datum)
        self.permanentDatumLineEdit.setText(self._well.permanent_datum)
        if self._well.permanent_datum_elevation is None: 
            self.permanentDatumElevationLineEdit.setText("")
        else:
            self.permanentDatumElevationLineEdit.setText(str(self._well.permanent_datum_elevation))
        #self.perm
        if self._well.elevation_above_permanent_datum is None: 
            self.elevationAbovePDLineEdit.setText("")
        else:
            self.elevationAbovePDLineEdit.setText(str(self._well.elevation_above_permanent_datum))        
        self.latitudeLineEdit.setText(self._well.latitude)
        self.longitudeLineEdit.setText(self._well.longitude)
        self.utmZoneLineEdit.setText(self._well.utm_zone)
        self.horizontalCoordinateSystemLineEdit.setText(self._well.horizontal_coordinate_system)
        if self._well.x_coordinate is None: 
            self.xCoordinateLineEdit.setText("")
        else:
            self.xCoordinateLineEdit.setText(str(self._well.x_coordinate))
        if self._well.y_coordinate is None: 
            self.yCoordinateLineEdit.setText("")
        else:
            self.yCoordinateLineEdit.setText(str(self._well.y_coordinate))
        
    def populateComboBoxes(self):
        #depth types eg MB, TVDSS etc
        depthTypes = ZAxis.getExtendedDataTypeUids()
        for item in depthTypes:
            self.depthTypeComboBox.addItem(str(item))
        
        #reference level eg DF, GL etc
        referenceLevelType = ReferenceLevelType.CBF
        refTypes = referenceLevelType.getAllTypeUids()
        for item in refTypes:
            self.depthReferenceComboBox.addItem(str(item))
            self.drillingReferenceComboBox.addItem(str(item))
            


        #eg m, ft etc
        depthUnits = LogType.getLogUnitsForType(LogType.DEPTH)
        for item in depthUnits:
            self.depthTypeUnitComboBox.addItem(str(item))
            self.depthReferenceUnitComboBox.addItem(str(item))
            self.elevationOfDepthReferenceUnitComboBox.addItem(str(item))
            self.tdDrillerUnitComboBox.addItem(str(item))
            self.waterDepthUnitComboBox.addItem(str(item))
            self.dfElevationUnitComboBox.addItem(str(item))
            self.kbElevationUnitComboBox.addItem(str(item))
            self.glElevationComboBox.addItem(str(item))
            self.permDatumElevUnitComboBox.addItem(str(item))
            self.elevationAbovePDComboBox.addItem(str(item))
            
    #set validators
      
    def setValidators(self):
        doubleValidator = QtGui.QDoubleValidator()
        intValidator = QtGui.QIntValidator()
        regexValidator = QtGui.QRegExpValidator()
        realValidator = RealValidator()
        #required
        self.wellNameLineEdit.setValidator(regexValidator)
        self.elevationOfDepthReferenceLineEdit.setValidator(doubleValidator)
        #optional
        self.areaLineEdit.setValidator(regexValidator)
        self.apiLineEdit.setValidator(regexValidator)
        self.blockLineEdit.setValidator(regexValidator)
        self.companyLineEdit.setValidator(regexValidator)        
        self.completionStatusLineEdit.setValidator(regexValidator)
        self.countryLineEdit.setValidator(regexValidator)
        self.countyLineEdit.setValidator(regexValidator)
        self.fieldLineEdit.setValidator(regexValidator)
        self.licenseLineEdit.setValidator(regexValidator)
        self.locationLineEdit.setValidator(regexValidator)
        self.operatorLineEdit.setValidator(regexValidator)
        self.provinceLineEdit.setValidator(regexValidator)
        self.stateLineEdit.setValidator(regexValidator)
        self.uwiLineEdit.setValidator(regexValidator)
        self.drillingContractorLineEdit.setValidator(regexValidator)
        self.rigNameLineEdit.setValidator(regexValidator)
        self.spudDateLineEdit.setValidator(regexValidator)
        self.tdDateLineEdit.setValidator(regexValidator)   
          
        self.tdDrillerLineEdit.setValidator(realValidator)       
        self.waterDepthLineEdit.setValidator(realValidator)
        self.dfElevationLineEdit.setValidator(realValidator)
        self.kbElevationLineEdit.setValidator(realValidator)
        self.glElevationLineEdit.setValidator(realValidator)     
        self.geodeticDatumLineEdit.setValidator(realValidator)
        self.permanentDatumLineEdit.setValidator(regexValidator)      
        self.permanentDatumElevationLineEdit.setValidator(realValidator)        
        self.elevationAbovePDLineEdit.setValidator(realValidator)       
        self.latitudeLineEdit.setValidator(regexValidator)
        self.longitudeLineEdit.setValidator(regexValidator)
        self.utmZoneLineEdit.setValidator(regexValidator)
        self.horizontalCoordinateSystemLineEdit.setValidator(regexValidator)        
        self.xCoordinateLineEdit.setValidator(realValidator)
        self.yCoordinateLineEdit.setValidator(realValidator)
             
    def connectSlots(self):
        ''' Connect Signal/Slots '''
        logger.debug(">>connectSlots()")

        #NB the filters need to be declared as self._filter= not as filter=

        self._focusOutFilter = FocusOutFilter()
        self.wellNameLineEdit.installEventFilter(self._focusOutFilter)  
        self._focusOutFilter.focusOut.connect(self.focusLostHandler)
        
        self.importOnlyRequiredDataRadioButton.clicked.connect(self.importOnlyRequiredDataRBClicked)
        self.importAllDataRadioButton.clicked.connect(self.importAllDataRBClicked)  
        self.newWellRadioButton.clicked.connect(self.newWellRadioButtonClicked)
        self.existingWellRadioButton.clicked.connect(self.existingWellRadioButtonClicked)
        
    def focusLostHandler(self):
        logger.debug(">>focusLost()")
        self.checkIfWellNameExists()
        #self.completeChanged.emit()


        
    def checkIfWellNameExists(self):
        ''' check is entered/existing well name already exists in the db '''
        logger.debug(">>checkIfWellNameExists()")
        if self._parent._wellExistsInDB:
            session = self._parent._session
            rs = session.query(Well, Well.name).all()
            for row in rs:
                if row.name == self.wellNameLineEdit.text():
                    logger.debug("Well name exists")
                    self.wellNameLineEdit.setFocus()
                elif str(row.name).lower == str(self.wellNameLineEdit.text()).lower:
                    QMessageBox.warning(QWidget, 'Existing well message', 'The well name is similar to an existing well. It is recommended to import this data into the existing well: '+row.name, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton)
                    logger.warn("The well name is similar to an existing well name. It is recommended to import this data into the existing well: "+row.name)
                    
   
    def importOnlyRequiredDataRBClicked(self, enabled):
        if enabled:
            self.scrollArea.setEnabled(False)
            self.importAllDataRadioButton.setChecked(False)
            self._parent._importAllData = False
        
    def importAllDataRBClicked(self, enabled):
        if enabled:
            self.scrollArea.setEnabled(True)
            self.importOnlyRequiredDataRadioButton.setChecked(False)
            self._parent._importAllData = True  
        
    def newWellRadioButtonClicked(self, enabled):
        if enabled:
            self.existingWellComboBox.setEnabled(False)
        
    def existingWellRadioButtonClicked(self, enabled):
        if enabled:
            self.existingWellComboBox.setEnabled(True)
            
    # required and non-required stata checking
    
    def attachNonRequiredCheckers(self):
        nonReqLineEdits = self.scrollArea.findChildren(QtGui.QLineEdit)
        for lineedit in nonReqLineEdits:
            lineedit.textChanged.connect(self.checkNonReqiredState)
            lineedit.textChanged.emit(lineedit.text())
            
    def attachRequiredCheckers(self):
        reqLineEdits = self.requiredGroupBox.findChildren(QtGui.QLineEdit)
        for lineedit in reqLineEdits:
            lineedit.textChanged.connect(self.checkReqiredState)
            lineedit.textChanged.emit(lineedit.text())
        
    def checkNonReqiredState(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        #Note all lineedits will have a validator
        if validator is not None:
            state = validator.validate(sender.text(), 0)[0]
            s = sender.text()
            if state == QtGui.QValidator.Acceptable and sender.text() is not "":
                color = ColorConstants.QLE_GREEN
                sender.setProperty('status', 'valid')
            elif state == QtGui.QValidator.Intermediate or sender.text() is "":
                color = ColorConstants.QLE_YELLOW
                sender.setProperty('status', 'valid')
            else:
                color = ColorConstants.QLE_RED
                sender.setProperty('status', 'invalid')
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            logger.debug("--checkState() no validator for: "+str(sender.objectName()))
            
    def checkReqiredState(self, *args, **kwargs):
        logger.debug(">>checkReqiredState()")
        sender = self.sender()
        logger.debug("--checkReqiredState() name: "+sender.objectName()+" type: "+str(type(sender)))
        validator = sender.validator()
        #Note all lineedits will have a validator
        if validator is not None:
            state = validator.validate(sender.text(), 0)[0]
            if state == QtGui.QValidator.Acceptable and sender.text() is not "":
                color = ColorConstants.QLE_GREEN
                sender.setProperty('status', 'valid')
            else:
                color = ColorConstants.QLE_RED
                sender.setProperty('status', 'invalid')
                #logger.debug("--checkReqiredState() invalid: "+sender.objectName)
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
            #For required fields update the enabled status of the next button
            self.completeChanged.emit()
        else:
            logger.debug("--checkState() no validator for: "+str(sender.objectName()))
                                       
    def isWellNameEmpty(self):
        if len(self.wellNameLineEdit.text()) == 0:
            logger.warn("A new well name is required if not adding to an existing well")
            self.wellNameLineEdit.setFocus()
            color = ColorConstants.QLE_RED
            self.wellNameLineEdit.setStyleSheet('QLineEdit { background-color: %s }' % color)
            return True
        return False
       
    # set default widget states
             
    def setDefaultState(self):
        self.setWellRadioButtons()      
        self.importAllDataRadioButton.setChecked(True)
        self.importAllDataRBClicked(True)

        
    def setComboInitialStates(self):
        #Depth type not well handled by .las format, user needs to specify
        #depthTypeComboBox defaults to MD which is first item in list
        #TODO need to detect if data is in seconds/milliseconds and default to TWT

        depthRefIndex = self.depthReferenceComboBox.findText(str(self._well.depth_reference), QtCore.Qt.MatchFixedString)
        if depthRefIndex >= 0:
             self.depthReferenceComboBox.setCurrentIndex(depthRefIndex)


        
    def setWellRadioButtons(self):
        ''' runs prior to user entering any data '''
        if self._parent._wellExistsInDB:
            existingWells = [self.existingWellComboBox.itemText(i) for i in range(self.existingWellComboBox.count())]
            if self.wellNameLineEdit.text() in existingWells:
                index = self.existingWellComboBox.findText(self.wellNameLineEdit.text())
                self.existingWellComboBox.setCurrentIndex(index)
                self.newWellRadioButton.setChecked(False)
                self.existingWellRadioButton.setChecked(True)
            else:
                #check if matches regardless of case and inform user
                existingWellsLowerCase = [x.lower() for x in existingWells]
                if str(self.wellNameLineEdit.text()).lower in existingWellsLowerCase:
                    logger.warn("A well with a similar name to: "+str(self.wellNameLineEdit.text())+" exists in the database")
                self.newWellRadioButton.setChecked(True)
                self.existingWellRadioButton.setChecked(False)
                self.existingWellRadioButton.setEnabled(False)
        else:
                self.newWellRadioButton.setChecked(True)
                self.existingWellRadioButton.setChecked(False)
                self.existingWellRadioButton.setEnabled(False)
            
         
    #override isComplete 
    def isComplete(self):
        logger.debug(">>isComplete()")  
        logger.debug("isComplete() "+ str(self.wizard()))
        pageValid = True
        reqLineEdits = self.requiredGroupBox.findChildren(QtGui.QLineEdit)
        for lineedit in reqLineEdits:
            if lineedit.property('status') == 'invalid':
                logger.debug(str(lineedit.objectName())+" is invalid")
                pageValid = False 
        return pageValid

       
    ''' 
    def nextButtonClicked(self):
        logger.debug(">>nextButtonClicked()")


        if self.checkIfWellNameIsEmpty():
            return
        else:
            self.populateWellObject()
    '''
      
    #populate well object
      
    def populateObject(self):
        logger.debug(">>populateObject()")
        #Required
        if self.newWellRadioButton.isChecked():
            self._well.name = self.wellNameLineEdit.text()
            self._well.existing = False
        else:
            self._well.name = self.existingWellComboBox.currentText()
            self._well.existing = True
        if self.existingWellRadioButton.isChecked():
            if not self._overwiteExistingData:
                #don't write any well data
                return
            
        self._well.z_measure_type_name = self.depthTypeComboBox.currentText()
        #TODO need to convert this to SI units
        self._well.depth_reference = self.depthReferenceComboBox.currentText()
        #if NumberUtils.isaNumber(self.elevationOfDepthReferenceLineEdit.text()):
        self._well.elevation_of_depth_reference=NumberUtils.parseStringToFloat(self.elevationOfDepthReferenceLineEdit.text(), None) 
        #else: 
           #self._well.elevation_of_depth_reference =  None
           
        if self.importAllDataRadioButton.isChecked():
            #Optional
            self._well.area = self.areaLineEdit.text()
            self._well.api = self.apiLineEdit.text()
            self._well.block = self.blockLineEdit.text()
            self._well.company = self.companyLineEdit.text()
            self._well.completion_status = self.completionStatusLineEdit.text()
            self._well.country = self.countryLineEdit.text()
            self._well.county = self.countyLineEdit.text()
            self._well.field = self.fieldLineEdit.text()
            self._well.license = self.licenseLineEdit.text()
            self._well.location = self.locationLineEdit.text()
            self._well.operator = self.operatorLineEdit.text()                                                     
            self._well.province = self.provinceLineEdit.text()
            self._well.state = self.stateLineEdit.text()
            self._well.uwi = self.uwiLineEdit.text()
            self._well.drilling_contractor = self.drillingContractorLineEdit.text()
            self._well.rig_name = self.rigNameLineEdit.text()
            self._well.spud_date = self.spudDateLineEdit.text()
            self._well.td_date = self.tdDateLineEdit.text()
            
            self._well.td_driller = NumberUtils.parseStringToFloat(self.tdDrillerLineEdit.text(), None)
            self._well.water_depth = NumberUtils.parseStringToFloat(self.waterDepthLineEdit.text(), None)    
            self._well.df_elevation = NumberUtils.parseStringToFloat(self.dfElevationLineEdit.text(), None)    
            self._well.kb_elevation = NumberUtils.parseStringToFloat(self.kbElevationLineEdit.text(), None)      
            self._well.gl_elevation = NumberUtils.parseStringToFloat(self.glElevationLineEdit.text(), None)     
            self._well.geodetic_datum = self.geodeticDatumLineEdit.text()
            self._well.permanent_datum = self.permanentDatumLineEdit.text()
            self._well.permanent_datum_elevation = NumberUtils.parseStringToFloat(self.permanentDatumElevationLineEdit.text(), None)
            self._well.elevation_above_permanent_datum = NumberUtils.parseStringToFloat(self.elevationAbovePDLineEdit.text(), None)       
            self._well.latitude = self.latitudeLineEdit.text()
            self._well.longitude = self.longitudeLineEdit.text()
            self._well.utm_zone = self.utmZoneLineEdit.text()
            self._well.horizontal_coordinate_system = self.horizontalCoordinateSystemLineEdit.text()
            self._well.x_coordinate = NumberUtils.parseStringToFloat(self.xCoordinateLineEdit.text(), None)
            self._well.y_coordinate = NumberUtils.parseStringToFloat(self.yCoordinateLineEdit.text(), None)   
   
    
class FocusOutFilter(QtCore.QObject):
    #see http://stackoverflow.com/questions/15066913/how-to-connect-qlineedit-focusoutevent
    focusOut = pyqtSignal()
    wellNameFocusOut = pyqtSignal()
    def eventFilter(self, widget, event):
        if event.type() == QEvent.FocusOut:
            if widget.objectName() == "wellNameLineEdit":
                self.focusOut.emit()
            return False
        else:
            return False
