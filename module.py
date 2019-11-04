import logging

logger = logging.getLogger(__name__)

def other_module_function():
    logger.info('called module_function from module.py (other module)')