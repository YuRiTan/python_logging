import os
import logging

from logging_utils import (
    setup_logging,
    setup_rotating_file_logger, 
    setup_timed_rotating_file_logger, 
    setup_stream_logger,
    setlevel_third_party_loggers,
    add_filter
)
from logging_filters import (
    BlacklistFilter,
    NoConnectionFilter
)
from module import (
    other_module_function, 
    function_that_triggers_pandas_warning,
    function_that_logs_from_third_party
)
from submodule.submodule import submodule_function


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
    setup_rotating_file_logger(logging.DEBUG, 'test.log', directory='logs')

    # Setting up timed rotating file logger which rotates log files depending on time (e.g. per day)
    # uses `logging.BasicConfig()`, which also logs to console by default
    # setup_timed_rotating_file_logger(logging.INFO, 'test.log')

    logger.info("Ready to start testing loggers")
    logger.info("Active root handlers: {}".format(logging.root.handlers))

    same_module_function()
    other_module_function()
    
    # Triggers a warning to stdout. Will show up in console, not in logfile.
    function_that_triggers_pandas_warning()

    # urllib3 uses python's logging module. You can therefore set the loglevel
    # differently to ignore certain logs for this specific library.
    # You can do this in different ways:

    # set the loglevel to different level for specific module
    # setlevel_third_party_loggers(include_prefix='urllib3', loglevel=logging.WARNING)

    # filter out logs by adding filter to a (log) handler
    # add_filter(BlacklistFilter(['urllib3']))

    # filter out logs as specified in `src.logging_filter.NoConnectionFilter`
    # add_filter(NoConnectionFilter())

    function_that_logs_from_third_party()
    submodule_function()
    logger.info("Done testing loggers")
