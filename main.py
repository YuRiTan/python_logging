import os
import logging
from logger_utils import (
    setup_logging,
    setup_rotating_file_logger, 
    setup_timed_rotating_file_logger, 
    setup_stream_logger
)
from module import other_module_function
from submudule.submodule import submodule_function

logger = logging.getLogger(__name__)

def same_module_function():
    logger.info('logging from function in same module')


if __name__ == '__main__':
    # Setting up stream logger using `logger_utils.setup_bare_logging()`, without `logging.BasicConfig()`
    # setup_stream_logger(logging.INFO)

    # Setting up stream logger using `logging_utils.setup_logger()`, which uses `logging.BasicConfig()`
    # setup_logging(logging.INFO)

    # Setting up rotating file logger which rotates log files depending on file size (e.g. max size 1Mb)
    # uses `logging.BasicConfig()`, which also logs to console by default
    setup_rotating_file_logger(logging.INFO, 'test.log')

    # Setting up timed rotating file logger which rotates log files depending on time (e.g. per day)
    # uses `logging.BasicConfig()`, which also logs to console by default
    # setup_timed_rotating_file_logger(logging.INFO, 'test.log')

    logger.info("Ready to start testing loggers")
    same_module_function()
    other_module_function()
    submodule_function()
    logger.info("Done testing loggers")