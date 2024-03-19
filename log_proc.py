import logging

import logging.config

# ------------LOGGER--------------
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s] %(asctime)s  <%(funcName)s>  %(message)s'
        },
    },

# ------Запись Log в файл---------------
    'handlers': {
       
        'FileHandler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            "filename": "main_log.log"
        },
        
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },
    
   

     'loggers': {
        'console_logger': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
         'file_logger': {
            'handlers': ['FileHandler'],
            'level': 'DEBUG',
            'propagate': True
        }
        
    }
}



#todo ssss



logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('console_logger')
logger.debug('Start log')

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

# ----------------------------------
