
from gui.widgets.okcanceldialog import OkCancelDialog
from gui.widgets.datalisttolistwidget import DataListToListWidget
from PyQt4.QtGui import QHBoxLayout, QStandardItemModel, QStandardItem,\
    QVBoxLayout, QRadioButton, QButtonGroup
from PyQt4.Qt import Qt

import logging


from db.core.well.well import Well
from statics.types.logtype import LogType
from preferences.general.generalsettings import GeneralSettings, WorkflowType
from statics.templates.wellplottype import WellPlotType
from globalvalues.appsettings import AppSettings
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from gui.wellplot.wellplotdialog.wellplotpg import WellPlotPG
from views.core.centraltabwidget import CentralTabWidget
logger = logging.getLogger('console')

class QuickPlotDialog(OkCancelDialog):
    '''
    Quick plot setup dialog
    '''
    SHOW_LOGS_IN_WELL = "Show logs in well"
    SHOW_LOGS_IN_LOG_SET = "Show logs in log set"
    SHOW_ALL_LOG_TYPES = "Show all log types"
    EXISTING_LOG_TYPES_MESSAGE = "Existing log types in black"
    
    def __init__(self, logs, well, quickTemplateName, logSet = None, parent=None):
        super(QuickPlotDialog, self).__init__(parent)
        self._logs = logs
        self._well = well
        self._quickTemplateName = quickTemplateName
        self._logSet = None
        self._template = None
        self._dataListToListWidget = None
        #show either logs or log types in left view
        self._logTypesInLeftView = False
        self.logsInWellRadioButton = None
        self.allLogTypesRadioButton = None
        self.generateTemplate()
        self.addWidgets()
        self.populateInitialData()
        self.connectSlots()
        
    def generateTemplate(self):
        #easier to use the WellPlotType for QUICKPLOT than database
        if self._quickTemplateName == WellPlotType.QUICKPLOT.name:
            quickPlotUid = WellPlotType.QUICKPLOT.uid
        elif self._quickTemplateName == WellPlotType.ALLLOGS.name:
            quickPlotUid = WellPlotType.ALLLOGS.uid
        elif self._quickTemplateName == WellPlotType.ACTIVELOGS.name:
            quickPlotUid = WellPlotType.ACTIVELOGS.uid
        elif self._quickTemplateName == WellPlotType.EMPTY.name:
            quickPlotUid = WellPlotType.EMPTY.uid
        else:
            logger.error("--handleQuickPlotChecked() no match for quickTemplateName: {0}".format(self._quickTemplateName))
            if AppSettings.isDebugMode:
                raise ValueError
        self._template = WellPlotTemplateDao.getWellPlotTemplateFromUid(quickPlotUid)
        
    def templateLogic(self):
        quickPlotUid = WellPlotType.QUICKPLOT.uid
        if self._template is None:
            logger.debug("No template found for uid:{0}".format(quickPlotUid))
        else:
            self._template.trackDataList = self.createQuickLogTypeMatrix()
        
    def addWidgets(self):
        self._dataListToListWidget = DataListToListWidget()
        vbox = QVBoxLayout()
        self.placeholderWidget.setLayout(vbox)
        vbox.addWidget(self._dataListToListWidget)
        self.addLogOrLogTypeOption()
        
    def addLogOrLogTypeOption(self):
        self.logsInWellRadioButton = QRadioButton()
        if self._logSet is None:
            self.logsInWellRadioButton.setText(self.SHOW_LOGS_IN_WELL)
        else:
            self.logsInWellRadioButton.setText(self.SHOW_LOGS_IN_LOG_SET)
        self.allLogTypesRadioButton = QRadioButton()
        self.allLogTypesRadioButton.setText(self.SHOW_ALL_LOG_TYPES)
        topButtonLayout = QHBoxLayout()
        self._dataListToListWidget.topButtonHolderWidget.setLayout(topButtonLayout)
        topButtonLayout.addWidget(self.logsInWellRadioButton)
        topButtonLayout.addWidget(self.allLogTypesRadioButton)
        topButtonGroup = QButtonGroup()
        topButtonGroup.addButton(self.logsInWellRadioButton)
        topButtonGroup.addButton(self.allLogTypesRadioButton)
        self.logsInWellRadioButton.setChecked(True)
        
    def populateInitialData(self):
        if self._logTypesInLeftView:
            self.logsInWellRadioButton.setChecked(True)
            self.logsInWellButtonClicked()
            self._dataListToListWidget.leftDataTypeListView.setToolTip(self.EXISTING_LOG_TYPES_MESSAGE)

        else:
            self.allLogTypesRadioButton.setChecked(True)
            self.allLogTypesButtonClicked()
            
    def generateLeftListLogModel(self):
        '''Returns log model using all logs in self._logs '''
        model = QStandardItemModel(self._dataListToListWidget.leftDataTypeListView)
        for log in self._logs:
            item = QStandardItem(log.name)
            # checkboxes are confusing
            item.setCheckable(False)
            model.appendRow(item)
        return model
            
        
    def generateLeftListLogTypeModel(self):
        '''Returns all LogType list model '''
        existingLogTypes = []
        logType = LogType.GAMMA
        #get type for each log
        if self._logs is not None and len(self._logs)>0:
            for log in self._logs:
                existingLogTypes.append(log.log_type_name)
        generalSettings = GeneralSettings()
        if generalSettings.workflowType == WorkflowType.petrophysics:
            logTypeList = logType.getAllLogTypesPetrophysicsStringList()
        elif generalSettings.workflowType == WorkflowType.rockphysics:
            logTypeList = logType.getAllLogTypesRockPhysicsStringList()
        else:
            logTypeList = logType.getAllLogTypesStringList()
            
        model = QStandardItemModel(self._dataListToListWidget.leftDataTypeListView)
        for logType in logTypeList:
            item = QStandardItem(logType)
            # checkboxes are confusing
            item.setCheckable(False)
            if logType not in existingLogTypes:
                item.setForeground(Qt.gray)
            model.appendRow(item)
        return model
        
    def createQuickLogTypeMatrix(self):
        logTypeMatrix = []
        for typeName in self.getRightListViewStrings():
            logTypeMatrix.append([typeName])
        return logTypeMatrix
    
    def logsInWellButtonClicked(self):
        leftModel = self.generateLeftListLogModel()
        self._dataListToListWidget.setLeftModel(leftModel)
        self._dataListToListWidget.rightListView.setModel(None)
        
    def allLogTypesButtonClicked(self):
        leftModel = self.generateLeftListLogTypeModel()
        self._dataListToListWidget.setLeftModel(leftModel)
        self._dataListToListWidget.rightListView.setModel(None)
    
    def connectSlots(self):
        self.logsInWellRadioButton.clicked.connect(self.logsInWellButtonClicked)
        self.allLogTypesRadioButton.clicked.connect(self.allLogTypesButtonClicked)

    def accept(self):
        if (self._dataListToListWidget.rightListView.model() is None) or (self._dataListToListWidget.rightListView.model().rowCount() == 0):
            logger.info("Please select logs to plot to continue")
        else:
            #need to connect WellPlotMPL to main application so can receive signals
            centralTabWidget = CentralTabWidget()
            wellPlotPG = WellPlotPG(logs= self._logs, well = self._well, template = self._template, logSet = self._logSet, parent = centralTabWidget)
            self.close()