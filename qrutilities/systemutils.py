import os, platform, subprocess, sys, re, getpass
import ctypes
from PyQt4 import QtGui
from PyQt4.QtGui import QDesktopWidget
from PyQt4.Qt import QX11Info

from globalvalues.constants.siconversionconstants import SIConversionConstants

import logging


logger = logging.getLogger('console')


PYTHON_V3 = sys.version_info >= (3,0,0) and sys.version_info < (4,0,0)
#[...]

class SystemUtils(object):
    '''
    classdocs
    '''
    
    #see http://stackoverflow.com/questions/4842448/getting-processor-information-in-python
    #untested
    @classmethod
    def getProcessorDetails(cls):
        if platform.system() == "Windows":
            return platform.processor()
        elif platform.system() == "Darwin":
            import os
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            command ="sysctl -n machdep.cpu.brand_string"
            return subprocess.check_output(command).strip()
        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).strip()
            #see http://stackoverflow.com/questions/24928908/python3-type-str-doesnt-support-the-buffer-api
            data = []
            data.append(all_info.decode('utf-8'))
            for line in data:
                line.split("\n")
                if "model name" in line:
                    return re.sub( ".*model name.*:", "", line,1)
        return ""

    @classmethod
    def availableCpuCount(cls):
        """ Number of available virtual or physical CPUs on this system, i.e.
        user/real as output by time(1) when called with an optimally scaling
        userspace-only program"""
    
        # cpuset
        # cpuset may restrict the number of *available* processors
        try:
            m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                          open('/proc/self/status').read())
            if m:
                res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
                if res > 0:
                    return res
        except IOError:
            pass
    
        # Python 2.6+
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass
    
        # http://code.google.com/p/psutil/
        try:
            import psutil
            return psutil.NUM_CPUS
        except (ImportError, AttributeError):
            pass
    
        # POSIX
        try:
            res = int(os.sysconf('SC_NPROCESSORS_ONLN'))
    
            if res > 0:
                return res
        except (AttributeError, ValueError):
            pass
    
        # Windows
        try:
            res = int(os.environ['NUMBER_OF_PROCESSORS'])
    
            if res > 0:
                return res
        except (KeyError, ValueError):
            pass
    
        # jython
        try:
            from java.lang import Runtime
            runtime = Runtime.getRuntime()
            res = runtime.availableProcessors()
            if res > 0:
                return res
        except ImportError:
            pass
    
        # BSD
        try:
            sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                      stdout=subprocess.PIPE)
            scStdout = sysctl.communicate()[0]
            res = int(scStdout)
    
            if res > 0:
                return res
        except (OSError, ValueError):
            pass
    
        # Linux
        try:
            res = open('/proc/cpuinfo').read().count('processor\t:')
    
            if res > 0:
                return res
        except IOError:
            pass
    
        # Solaris
        try:
            pseudoDevices = os.listdir('/devices/pseudo/')
            res = 0
            for pd in pseudoDevices:
                if re.match(r'^cpuid@[0-9]+$', pd):
                    res += 1
    
            if res > 0:
                return res
        except OSError:
            pass
    
        # Other UNIXes (heuristic)
        try:
            try:
                dmesg = open('/var/run/dmesg.boot').read()
            except IOError:
                dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
                dmesg = dmesgProcess.communicate()[0]
    
            res = 0
            while '\ncpu' + str(res) + ':' in dmesg:
                res += 1
    
            if res > 0:
                return res
        except OSError:
            pass
    
        raise Exception('Can not determine number of CPUs on this system')
    
    @classmethod
    def getScreenGeometry(cls):
        '''Return a QRect'''
        screenRect = QtGui.QDesktopWidget().screenGeometry()
        return screenRect
    
    @classmethod
    def getScreenDPI(cls):
        defaultScreen = -1
        dpiX = QX11Info.appDpiX(defaultScreen)
        dpiY = QX11Info.appDpiX(defaultScreen)
        return dpiX, dpiY
    
    @classmethod
    def getScreenDPMM(cls):
        '''Screen dots per mm'''
        dpiX, dpiY = SystemUtils.getScreenDPI()
        assert SIConversionConstants.MM_PER_INCH != 0
        return float(dpiX)/SIConversionConstants.MM_PER_INCH, float(dpiY)/SIConversionConstants.MM_PER_INCH
    
    @classmethod
    def getScreenDPMetre(cls):
        '''screen dots per metre'''
        dpX, dpY = SystemUtils.getScreenDPI()
        return float(dpX)/0.0254, float(dpY)/0.0254
    
    @classmethod
    def getScreenDPCM(cls):
        '''screen dots per cm'''
        dpmmX, dpmmY = SystemUtils.getScreenDPMM()
        return dpmmX*10, dpmmY*10
            

    @classmethod
    def getCurrentUser(cls):
        return getpass.getuser()

    
                                
        