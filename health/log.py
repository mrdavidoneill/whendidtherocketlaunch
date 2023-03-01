"""
This module sets up logging for the whendidtherocketlaunch_bot Telegram bot. 
It defines a logger object and adds two handlers to it: 
    - console handler
        logs messages with a debug level or higher
    -  file handler
        logs messages with an info level or higher. 
        
    The log messages are formatted with a time stamp, logger name, log level, 
    and message. The log file is stored in the logs directory with the name 
    whendidtherocketlaunch_bot.log.
"""
import logging
import logging.handlers
import time
import os

######### DEBUG LEVELS ##########
CONSOLE_LEVEL = logging.DEBUG
FILE_LEVEL = logging.INFO
#################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
formatter.converter = time.gmtime

# Log to console
ch = logging.StreamHandler()
ch.setLevel(CONSOLE_LEVEL)
ch.setFormatter(formatter)
logger.addHandler(ch)

# Log to file
filepath = os.path.join(
    os.path.dirname(__file__), *["logs", "whendidtherocketlaunch_bot.log"]
)
fh = logging.handlers.RotatingFileHandler(filepath, maxBytes=1024 * 8, backupCount=1)
fh.setLevel(FILE_LEVEL)
fh.setFormatter(formatter)
logger.addHandler(fh)
