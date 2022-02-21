"""
Logging helper class
"""

import os
import logging as log

LOG_DIR = str(os.getcwd())+"\\logs\\"

def log_setup(logger_name, log_file, mode='a'):
    """
    Configure a new logger and return the new instance to the user

    Args:
        logger_name (str): User defined name for the Logger obj instance
        log_file (str): Name for the log_file
        mode (str, optional): Log mode. Recommended: 'w'rite or 'a'ppend. Defaults to 'w'.

    Returns:
        log.Logger: New log file instance the user can write to
    """
    
    #   Initialize handlers
    new_log = log.getLogger(logger_name)
    formatter = log.Formatter("[%(asctime)s] %(message)s")
    file_handler = log.FileHandler(log_file, mode=mode)
    file_handler.setFormatter(formatter)
    stream_handler = log.StreamHandler()

    #   Create logging object with handlers
    new_log.setLevel(log.DEBUG)
    new_log.addHandler(file_handler)
    new_log.addHandler(stream_handler)
    return new_log

class Logger():
    """
    Logger object that allows a user to quickly define a new instance and log results to the file
    """
    def __init__(self, key="none"):
        """
        Constructor

        Args:
            log (str, optional): Log type. Defaults to "debug".
            assignment (str, optional): Assignment/Name of the logger. Defaults to "none".
        """
        self.log_obj = log_setup(f"{key}", LOG_DIR+f"{key}.log")
        
    def __call__(self, logStr):
        """
        Call the object to have a message immidiately logged to the debug output

        Args:
            logStr (str): Message to add to the logfile
        """
        self.log_obj.info(logStr)
        
    def log(self, logStr):
        """
        Log a debug string to the specified log file

        Args:
            logStr (str): String to add to logfile
        """
        self.log_obj.debug(logStr)
        
    def info(self, logStr):
        """
        Log an info string to the specified log file

        Args:
            logStr (str): String to add to logfile
        """
        self.log_obj.info(logStr)