import logging


class NoConnectionFilter(logging.Filter):
    """ Filters out all logs that contain 'connection' in the module name """
    def filter(self, record):
        return not 'connection' in record.name

        
class WhitelistFilter(logging.Filter):
    def __init__(self, whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)


class BlacklistFilter(logging.Filter):
    def __init__(self, blacklist):
        self.blacklist = [logging.Filter(name) for name in blacklist]

    def filter(self, record):
        return not any(f.filter(record) for f in self.blacklist)