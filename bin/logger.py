"""
Logging helper class
"""

import os
import logging as log

LOG_DIR = str(os.getcwd())+"\\logs\\"

def log_setup(logger_name: str, log_file: str, mode: str='w'):
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
    formatter = log.Formatter("[%(levelname)s]\t[%(asctime)s] %(message)s")
    file_handler = log.FileHandler(log_file, mode=mode)
    file_handler.setFormatter(formatter)
    stream_handler = log.StreamHandler()

    #   Create logging object with handlers
    new_log.setLevel(log.DEBUG)
    new_log.addHandler(file_handler)
    new_log.addHandler(stream_handler)
    return new_log

class Logger():
    """Logger object that allows a user to quickly define a new instance and log results to the file"""
    
    def __init__(self, key: str="none"):
        """Constructor for log object. Takes a name for the file and handles the rest of the
        setup internally.

        Args:
            key (str, optional): Assignment/Name of the logger. Defaults to "none".
        """
        self.log_obj = log_setup(f"{key}", LOG_DIR+f"{key}.log")
        
    def __call__(self, logStr: str, mode: str='i'):
        """
        Call the object to have a message immidiately logged to the debug output

        Args:
            logStr (str): Message to add to the logfile
            mode (str, optional): Logging mode for the file. Defaults to 'i' for Info
        """
        if mode == 'i':
            self.log_obj.info(logStr)
        elif mode == 'd':
            self.log_obj.debug(logStr)
        elif mode == 'e':
            self.log_obj.error(logStr)
        elif mode == 'w':
            self.log_obj.warning(logStr)
        else:
            self.log_obj.info(logStr)

        
    def log(self, logStr: str):
        """
        Log a debug string to the specified log file

        Args:
            logStr (str): String to add to logfile
        """
        self.log_obj.debug(logStr)
        
    def info(self, logStr: str):
        """
        Log an info string to the specified log file

        Args:
            logStr (str): String to add to logfile
        """
        self.log_obj.info(logStr)

    def error(self, logStr: str):
        """Log an error string to the log file

        Args:
            logStr (str): String to add to the logfile
        """
        self.log_obj.error(logStr)

    def debug(self, logStr: str):
        """Log an debug string to the log file

        Args:
            logStr (str): String to add to the logfile 
        """
        self.log_obj.debug(logStr)

    def warning(self, logStr: str):
        """Log an warning string to the log file

        Args:
            logStr (str): String to add to the logfile 
        """
        self.log_obj.warning(logStr)