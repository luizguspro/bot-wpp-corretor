import logging
import os
from datetime import datetime

def setup_logger():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))
    
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    os.makedirs('logs', exist_ok=True)
    file_handler = logging.FileHandler(
        f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(console_format)
    logger.addHandler(file_handler)
    
    return logger
