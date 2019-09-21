#!/usr/bin/env python
""" generated source for module AppSettings """



from io import IOBase
import os, platform, subprocess, sys, re
from PyQt4.QtGui import QDesktopWidget
from PyQt4.QtCore import QDir, QFileInfo
from os import path
import loggerpackage
from qrutilities.systemutils import SystemUtils


#in java version was located at statics.project.AppSettings
class AppSettings(object):
    """ generated source for class AppSettings """
    developerMode = False
    databaseServerMode = False
    newProjectFirstMainConnection = False
    #developer debug
    isDebugMode = True
    isUnitTest = True
    #skips deprecated code tests is true
    skipDeprecatedTests = True
    #add this setting to allow user to change logger to debug level?
    #isUserDebugMode = False
    date = str()

    sevenDaysInMilliSeconds = 604800000
    isWindowsVista = False
    isWindows = False
    isLinux = False
    isUnix = False
    isMultiProcessor = False
    processorName = platform.processor()
    IMAGE_PATH = os.environ.get("IMAGE_PATH")
    ACTIONS_ICON_PATH = IMAGE_PATH+"toolbarButtons/actions/16x16/"
    softwareName = "Avoca"
    companyName = "qReservoir"
    softwareVersion = "0.4.0"
    databaseVersion = "0.2.3"
    #the following should be automatically generated on build
    buildNumber = "Unknown"
    buildDate = "20150704"
    
    pythonRuntimeVersion = sys.version_info
    installDir = IOBase
    workingFile = ""
    projectFile = ""
    searchProjectDir = ""
    tempDir = IOBase
    dataDir = IOBase
    logFile = IOBase
    globalSettingsDirectory = IOBase
    applicationName = "qReservoir"
    autoSaveTimeMs = 0
    externalFilesDir = IOBase
    DATE_FORMAT = "YYYY-MM-dd_hh-mm-ss"
    #activeShell = Shell()
    FOLDER_NAME = "qr"
    osName = os.name
    DATABASE_PROTOCOL = "sqlite:///"
    QR_DATABASE_NAME = "/tmp/pyqr.db"

    START_ON_SECOND_SCREEN = True
    #defaults, reset by main class
    screenWith = 1024
    screenHeight = 768

    
    
    
    
    @classmethod
    def getLoggingConfig(cls):
        """Returns the absolute path to the logging config file
        """
        return path.join(path.split(loggerpackage.__file__)[0], 'logging.conf')

    '''
    @classmethod
    def makeDataAndInstallDirs(cls):
        """ generated source for method makeDataAndInstallDirs """
        try:
            cls.dataDir = File((StringBuilder()).append(System.getProperty("user.home")).append(File.separator).append("qr").__str__())
            cls.installDir = File(file_.getParent())
            cls.dataDir.mkdirs()
        except Exception as e:
            cls.logger.error("Error: Error creating File. " + e)

    @classmethod
    def windowsHandler(cls, osName):
        """ generated source for method windowsHandler """
        file1 = File((StringBuilder()).append(System.getProperty("user.home")).append(File.separator).append("qr").__str__())
        if not cls.dataDir.exists() and file1.exists():
            try:
                FileIO.copyDir(file1, cls.dataDir)
            except Exception as exception:
                cls.logger.warn("Warn: Closing application. " + exception)
        cls.isWindows = True
        if osName.lower() == "windows vista":
            cls.isWindowsVista = True

    @classmethod
    def makeLogFolderAndFile(cls):
        """ generated source for method makeLogFolderAndFile """
        logFolder = File(cls.dataDir, "log")
        logFolder.mkdirs()
        s1 = StringOps.validateName(StringOps.getDateAndTime())
        cls.logFile = File(logFolder, (StringBuilder()).append("qr").append(s1).append(".log").__str__())

    @classmethod
    def makeTempDir(cls):
        """ generated source for method makeTempDir """
        corePropertyTempDirName = CorePropertyFileManager.getTempDir()
        if corePropertyTempDirName == None or corePropertyTempDirName == "" or not (File(corePropertyTempDirName)).exists():
            cls.tempDir = File(System.getProperty("java.io.tmpdir"))
            if not cls.tempDir.exists():
                if AppModel.isDebugMode():
                    cls.logger.debug("--initializeStatics(): No Temp Dir ")
        else:
            cls.tempDir = File(corePropertyTempDirName)

    @classmethod
    def makeGlobalSettingsDir(cls):
        """ generated source for method makeGlobalSettingsDir """
        globalSettingsDirName = CorePropertyFileManager.getGlobalSettingsDir()
        if globalSettingsDirName == None or globalSettingsDirName == "" or not (File(globalSettingsDirName)).exists():
            cls.globalSettingsDirectory = File(cls.dataDir.getAbsolutePath())
        else:
            cls.globalSettingsDirectory = File(globalSettingsDirName)


    @classmethod
    def setAutosaveTime(cls):
        """ generated source for method setAutosaveTime """
        autoSaveTime = CorePropertyFileManager.getAutoSaveTime()
        if autoSaveTime != None and autoSaveTime != "":
            try:
                cls.autoSaveTimeMs = Integer.parseInt(autoSaveTime)
            except NumberFormatException as numberformatexception:
                cls.autoSaveTimeMs = 0x2bf20

    '''



