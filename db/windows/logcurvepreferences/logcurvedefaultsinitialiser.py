
import logging

from statics.types.logtype import LogType


from statics.types.domain import Domain
from globalvalues.constants.plottingconstants import PlottingConstants,\
    PenLineStyles, PGPointStyles
from globalvalues.appsettings import AppSettings

from db.windows.logcurvepreferences.logcurvepreferences import LogCurvePreferences

from db.core.basedao import BaseDao



logger = logging.getLogger('console')

class LogCurveDefaultsInitialiser(object):
    '''
    Persists default values in database
    '''

    def __init__(self, session, params=None):
        #if session is None:
        #   session = self.getSession()
        self._session = session
        self._initialiseLogCurveDefaults()
        #if doCommit:
        #    self.commitSession(self.session)
            
    def _initialiseLogCurveDefaults(self):
        logger.debug(">>_initialiseLogCurveDefaults()")
        domain = Domain
        logarithmicScale = False
        rgb_values = self.createRGBvalues()
        for uid in LogType.getLogTypeUids():
            #logger.debug("--_initialiseLogCurveDefaults() uid: "+str(uid))
            logCurveData = LogCurvePreferences()
            logType = LogType.getLogTypeFromUid(uid)
            logCurveData.log_type_uid = uid
            logCurveData.log_type_name = logType.name
            
            logCurveData.log_plot_left = logType.getDefaultLogPlotRange().getStart()
            logCurveData.log_plot_right = logType.getDefaultLogPlotRange().getStop()
            logCurveData.log_plot_default = logType.defaultValue
            logCurveData.log_plot_points_on = False
            logCurveData.histogram_left = logType.getDefaultLogPlotRange().getStart()
            logCurveData.histogram_right = logType.getDefaultLogPlotRange().getStop()
            logCurveData.histogram_default = logType.defaultValue
            logCurveData.cross_plot_left = logType.getDefaultLogPlotRange().getStart()
            logCurveData.cross_plot_right = logType.getDefaultLogPlotRange().getStop()
            logCurveData.cross_plot_default = logType.defaultValue
            
            logCurveData.line_width = PlottingConstants.LOG_LINE_WIDTH
            logCurveData.line_style = PlottingConstants.LOG_LINE_STYLE
            logCurveData.point_size = PlottingConstants.LOG_MARKER_SIZE
            logCurveData.point_style = PGPointStyles.circle.name
            #add color to logType
            logCurveData.rgb = self.valueOrRaise(rgb_values, uid)
            logCurveData.alpha = logType.alpha
            #change logType mnems to csv
            logCurveData.log_types = logType.curveMnemonic
            if logType.domain == domain.RESISTIVITY:
                logarithmicScale = True
                logCurveLogCyles = PlottingConstants.LOG_CYCLES
            logCurveData.is_logarithmic = logarithmicScale
            #is default not preferences
            logCurveData.is_preferences = False
            
            self._session.add(logCurveData)
            self._session.flush()
           
    def valueOrRaise(self, data, key):
        value = data.get(key)
        if value is None:
            logger.error("--valueOrRaise Error")
            if AppSettings.isDebugMode:
                raise KeyError("%s not present" % key)
        return value 

    def createRGBvalues(self):
        #see colours here http://cloford.com/resources/colours/500col.htm
        rgb_values = {}
        rgb_values['unknown'] = "0,0,0"
        rgb_values['vp'] = "21,  21, 196"
        rgb_values['vs'] = "0, 255, 255"
        rgb_values['gamma'] = "33, 179,  33"
        rgb_values['rho'] = "242,  26,  26"
        rgb_values['porosity'] = "21,  21, 196"
        rgb_values['volumefraction'] = "243, 132, 132"
        rgb_values['saturation'] = "255, 153, 18"
        rgb_values['cal'] = "200, 200, 200"
        rgb_values['dt'] = "0, 0, 255"
        rgb_values['dts'] = "0, 255, 0"
        rgb_values['temp'] = "255, 255, 0"
        rgb_values['resis'] = "255, 0, 0"
        rgb_values['acimp'] = "242,  26,  26"
        rgb_values['presformation'] = "255, 128, 0"
        rgb_values['mod'] = "128, 0, 255"
        rgb_values['perm'] = "0, 214, 255"
        rgb_values['sal'] = "150, 150, 150"
        rgb_values['gor'] = "242,  26,  26"
        rgb_values['oden'] = "255, 128, 0"
        rgb_values['depth'] = "0,0,0"
        rgb_values['time'] = "0,0,0"
        rgb_values['poissonratio'] = "219, 128,   4"
        rgb_values['eimp'] = "219, 128,   4"
        rgb_values['saturationset'] = "0, 255, 0"
        rgb_values['volumefractionset'] = "21,  21, 196"
        rgb_values['reflect'] = "150, 150, 150"
        rgb_values['misc'] = "255, 0, 0"
        rgb_values['trace'] = "0,0,0"
        rgb_values['thomsen'] = "255, 0, 255"
        rgb_values['sp'] = "255, 170,   0"
        rgb_values['epsilonani'] = "255,   0, 240"
        rgb_values['deltaani'] = "243, 132, 132"
        rgb_values['gammaani'] = "242,  26,  26"
        rgb_values['preshydrostatic'] = "255, 128, 0"
        rgb_values['preslithostatic'] = "0, 255, 0"
        rgb_values['presves'] = "114,  40,   3"   
        rgb_values['presfracture'] = "255,   0, 240"
        rgb_values['porosityneutron'] = "0, 0, 255"   
        rgb_values['facies'] = "0,0,0"
        rgb_values['horizontaldist'] = "242,  26,  26"
        rgb_values['coordinatedist'] = "200, 200, 200"
        rgb_values['lithology'] = "255, 255, 0"
        rgb_values['ai'] = "255, 0, 0"
        rgb_values['gi'] = "33, 179,  33"
        rgb_values['si'] = "255, 170,   0"
        rgb_values['eei'] = "0, 0, 255"
        rgb_values['ei2'] = "243, 132, 132"
        rgb_values['ei3'] = "21,  21, 196"
        rgb_values['sei2'] = "255, 128, 0"
        rgb_values['sei3'] = "33, 179,  33"
        rgb_values['m'] = "243, 132, 132"
        rgb_values['mu'] = "219, 128,   4"
        rgb_values['k'] = "255, 170,   0"
        rgb_values['lambda'] = "0, 255, 255"
        rgb_values['e'] = "114,  40,   3"
        rgb_values['angle'] = "33, 179,  33"
        rgb_values['lambdarho'] = "33, 179,  33"
        rgb_values['murho'] = "0, 0, 255"
        rgb_values['lambdaovermu'] = "0, 255, 255"
        rgb_values['modulusshearmu'] = "30,  30, 30"
        rgb_values['modulusyoungse'] = "30,  30, 30"
        rgb_values['modulusm'] = "30,  30, 30"
        rgb_values['moduludbulkk'] = "30,  30, 30"
        rgb_values['pressuregradient'] = "0,0,0"
        rgb_values['mudweight'] = "114,  40,   3"
        rgb_values['wellcasing'] = "200, 200, 200"
        rgb_values['emcommonoffset'] = "0, 0, 255"
        rgb_values['emrta'] = "200, 200, 200"
        rgb_values['anisotropysystem'] = "0, 214, 255"
        rgb_values['mobility'] = "0, 255,  11"
        rgb_values['densitycorrection'] = "242,  26,  26"
        rgb_values['photoelectriceffect'] = "255, 170,   0"
        rgb_values['porositydensity'] = "153, 186, 243"
        rgb_values['porositysonic'] = "153, 186, 243"        
        rgb_values['resismedium'] = "255, 0, 240"
        rgb_values['resisshallow'] = "219, 128,   4"
        rgb_values['resisdeep'] = "255, 0, 0"
        rgb_values['mass'] = "0,0,0"
        rgb_values['size'] = "0,0,0"
        rgb_values['fluidvolume'] = "21,  21, 196"
        rgb_values['capturecrosssectionapparentmatrix'] = "30,  30, 30"
        rgb_values['dtapparentmatrix'] = "30,  30, 30"
        rgb_values['densityapparentmatrix'] = "30,  30, 30"
        rgb_values['dtapparentfluid'] = "30,  30, 30"
        rgb_values['lithologym'] = "50,  50, 50"
        rgb_values['lithologyn'] = "150,  150, 50"
        rgb_values['epsilon'] = "150,  50, 50"
        rgb_values['mudgas'] = "100, 100, 100"
        rgb_values['projtn'] = "80, 80, 80"
        rgb_values['undefined1'] = "30,  30, 30"
        rgb_values['undefined2'] = "30,  30, 30"
        rgb_values['undefined3'] = "30,  30, 30"
        rgb_values['undefined4'] = "30,  30, 30"
        return rgb_values
    
    #TODO connect this method
    def _generateDefaultTemplateLogString(self):
        _defaultTypes = [LogType.CAL, LogType.DT, LogType.GAMMA, LogType.PHOTOELECTRIC_EFFECT, LogType.POROSITY, LogType.POROSITY_NEUTRON, LogType.RESIS, LogType.RHO]   
        _uids = []
        for logType in _defaultTypes:
            _uids.append(logType.getUid())  
        _defaultLogPlotUidString = " ".join(_uids)
        return _defaultLogPlotUidString
    