import logging

class AnsiColorCodes:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
#Debugからerrorのレベルまで対応
class ColorFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__(fmt)

    def format(self, record):
        color = ''
        if record.levelno == logging.WARNING:
            color = AnsiColorCodes.WARNING
        elif record.levelno == logging.ERROR:
            color = AnsiColorCodes.FAIL
        elif record.levelno == logging.INFO:
            color = AnsiColorCodes.OKGREEN
        elif record.levelno == logging.DEBUG:
            color=AnsiColorCodes.OKBLUE

        record.msg = f"{color}{record.msg}{AnsiColorCodes.ENDC}"
        return super().format(record)
    
logger=logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter('%(levelname)s: %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)