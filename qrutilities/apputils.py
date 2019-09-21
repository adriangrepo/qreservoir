
from os import path


#and http://blog.toddysm.com/2012/09/configuring-logging-in-python-the-real-life-example.html
def get_logging_config():
    """Returns the absolute path to the logging config file
    """
    return path.join(path.split(qr.__file__)[0], 'logging.conf')