import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import StreamHandler
import os

LOG_FMT_COLOR = ("\33[36m[%(asctime)s] \33[33m[%(levelname)s] \33[35m%(name)s "
                 "\33[34m%(filename)s:%(funcName)s:%(lineno)d\033[0m %(message)s")
LOG_FMT = ("[%(asctime)s] [%(levelname)s] %(name)s %(filename)s:"
           "%(funcName)s:%(lineno)d %(message)s")
DATE_FMT = "%Y-%m-%d %H:%M:%S"
 

logger = logging.getLogger()


def setup_bare_logging(loglevel):
    """ setting up (root) logger without any handlers 
    
    Notes
    -----
    This could also be done using:
    ```
    logging.basicConfig(
        level=loglevel,
        handlers=[]  # removes the stream handler automatically made by basicConfig
    )
    ```
    """

    for h in logging.root.handlers:
        logging.root.removeHandler(h)
    logging.root.setLevel(loglevel)


def setup_stream_logger(loglevel):
    """ For illustration purposes, sets up a logger with StreamHander and specified formatting
    to show what :func:`logging.BasicConfig()` basically does (except for the formatting).
    """

    setup_bare_logging(loglevel)
    handler = StreamHandler()
    formatter = logging.Formatter(LOG_FMT_COLOR)
    handler.setFormatter(formatter)
    handler.setLevel(loglevel)
    logging.root.addHandler(handler)


def setup_logging(loglevel):
    """ setting up (root) logger with default stream handler using :func:`logging.basicConfig()` 
    
    Notes
    -----
    In case you want to add handlers (e.g. FileHandler) afterwards, that is perfectly fine. 
    Please keep in mind that the StreamHandler is active as well.
    
    """

    # This function does nothing if the root logger already has handlers configured.
    # Source :func:`logging.basicConfig()`
    for h in logging.root.handlers:
        logging.root.removeHandler(h)

    logging.basicConfig(
        level=loglevel,
        format=LOG_FMT_COLOR,
        datefmt=DATE_FMT,
    )


def check_logdir(directory):
    try:
        directory = os.path.normpath(directory)
    except TypeError as te:
        logger.warning("Provided invalid directory. Setting "
                       "logdir to current working directory."
                       " Original error: {}".format(te))
        directory = '.'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def setup_rotating_file_logger(loglevel, fname, directory=None, **rfh_kwargs):
    """ Sets root logger, and creates RotatingFileHandler with format defined by
    the `LOG_FMT` constant from this module.
    """
    setup_logging(loglevel)
    directory = check_logdir(directory)
    handler = RotatingFileHandler(
        os.path.join(directory, fname), 
        maxBytes=rfh_kwargs.get('maxBytes', 1_000_000),
        backupCount=rfh_kwargs.get('backupCount', 2)
    )

    file_formatter = logging.Formatter(LOG_FMT)
    handler.setFormatter(file_formatter)
    handler.setLevel(loglevel)
    logging.root.addHandler(handler)


def setup_timed_rotating_file_logger(loglevel, fname, directory=None, **trfh_kwargs):
    """ Sets root logger, and creates TimedRotatingFileHandler with format defined 
    by :func:`get_log_format()` from this module.
    """
    setup_logging(loglevel)
    directory = check_logdir(directory) 
    handler = TimedRotatingFileHandler(
        os.path.join(directory, fname), 
        when=trfh_kwargs.get('when', 'D'),
        interval=trfh_kwargs.get('interval', 1),
        backupCount=trfh_kwargs.get('backupCount', 30)
    )
    file_formatter = logging.Formatter(LOG_FMT)
    handler.setFormatter(file_formatter)
    handler.setLevel(loglevel)
    logging.root.addHandler(handler)


def setlevel_third_party_loggers(prefix, loglevel=logging.WARNING):
    """ Sets loglevel of (third party) loggers (with a certain prefix like `sklearn`)
    to certain level. This is often done when loglevel is set to DEBUG, but you 
    would like to set a different loglevel to this third party logger.
    """
    for name in logging.root.manager.loggerDict:
        if name.startswith(prefix):
            logging.getLogger(name).setLevel(loglevel)


def add_filter(filter_):
    """ Utility function that adds a filter to all root handlers """
    for handler in logging.root.handlers:
        handler.addFilter(filter_)
