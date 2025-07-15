import os
import logging
import logging.config

from config.settings import settings


def setup_logging():
    """设置日志配置"""
    os.makedirs(settings.LOG.DIR, exist_ok=True)
    
    log_file = os.path.join(settings.LOG.DIR, 'INFO.log')
    error_log_file = os.path.join(settings.LOG.DIR, 'ERROR.log')
    
    config_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': settings.LOG.FORMAT
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': log_file,
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf8'
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': error_log_file,
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf8'
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file', 'error_file'],
                'level': settings.LOG.LEVEL,
                'propagate': True
            },
            'uvicorn': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'uvicorn.error': {
                'handlers': ['console', 'error_file'],
                'level': 'ERROR',
                'propagate': False
            },
            'uvicorn.access': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }
    
    logging.config.dictConfig(config_dict)
    return config_dict

