import logging

import logging.config

# ------------LOGGER--------------
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(name)s  %(funcName)s  %(message)s'
        },
    },

    'handlers': {
        'FileHandler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            "filename": "log_my.log"
        },
    },
    
    # 'handlers': {
    #     'stream_handler': {
    #         'class': 'logging.StreamHandler',
    #         'formatter': 'default_formatter',
    #     },
    # },

    'loggers': {
        'my_logger': {
            'handlers': ['FileHandler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_logger')
logger.debug('Start log')

# ----------------------------------
