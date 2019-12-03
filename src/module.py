import logging
import pandas as pd
import urllib3

logger = logging.getLogger(__name__)

def other_module_function():
    logger.info('called module_function from module.py (other module)')

def function_that_triggers_pandas_warning():
    """ Function that demonstrates Warnings triggered by thirt party
    modules. 
    
    Notes
    -----
    These warnings will be redirected to `stderr` and will therefore show
    in between StreamLogger logs, but not in logs written to file.
     """
    df = pd.DataFrame({'A': [1,2], 'B': [3,4]})
    df[df['A'] == 1]['B'] = 100  # should trigger a SettingWithCopyWarning

def function_that_logs_from_third_party():
    """ In case you use a Python Module that uses Python's logging module
    the logs will appear in between our logs too. This is because we capture
    our logs using the root logger. You can remove them for example by setting
    the loglevel differently on module level as shown below. 
    
    Example
    -------
    `urllib3.connectionpool` triggers DEBUG logs, you could set urllib3 
    to loglevel WARNING for example:
    
    >>> logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    """
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://httpbin.org/robots.txt')
