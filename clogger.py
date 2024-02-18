#!/usr/bin/env python3

from logging.handlers import RotatingFileHandler
from dataclasses import dataclass
import logging
import sys
import os


@dataclass
class mods:
    _aqua: str = '\x1b[36;20m'
    _green: str = '\x1b[32;20m'
    _yellow: str = '\x1b[33;20m'
    _red: str = '\x1b[31;20m'
    _uncolor: str = '\x1b[0m'
    _bold: str = '\033[1m'
    _unbold: str = '\033[0m'

    def bold(self, text: str) -> str:
        return f'{self._bold}{text}{self._unbold}'

    def aqua(self, text: str) -> str:
        return f'{self._aqua}{self._bold}{text}{self._unbold}{self._uncolor}'

    def green(self, text: str) -> str:
        return f'{self._green}{self._bold}{text}{self._unbold}{self._uncolor}'

    def yellow(self, text: str) -> str:
        return f'{self._yellow}{text}{self._uncolor}'

    def red(self, text: str) -> str:
        return f'{self._red}{text}{self._uncolor}'


class ColorFormatter(logging.Formatter):
    def __init__(self, *args: str, **kwargs: str) -> None:
        super().__init__(*args, **kwargs)
        
        GREY = "\x1b[36;20m"
        GREEN = "\x1b[32;20m"
        YELLOW = "\x1b[33;20m"
        RED = "\x1b[31;20m"
        BOLD_RED = "\x1b[31;1m"

        self.colors = {
            logging.DEBUG: GREY,
            logging.INFO: GREEN,
            logging.WARNING: YELLOW,
            logging.ERROR: RED,
            logging.CRITICAL: BOLD_RED,
        }
        self._fmts = {
            level: self.add_colors(level) for level in self.colors
        }

    def add_colors(self, level: int) -> str:
        _color = self.colors[level]
        RESET = "\x1b[0m"
        return self._style._fmt.replace('#c', _color).replace('#r', RESET)

    def format(self, record: int) -> str:
        self._style._fmt = self._fmts[record.levelno] 
        return super().format(record)


def max_len():
    maxlen = max([
        len(x.name.split('.py')[0]) for x in os.scandir('.') \
        if x.name.endswith('.py') and x.is_file()
    ])
    if maxlen > 1:
        return maxlen
    else:
        return 5


def log(
        level: str = 'INFO',
        logdir: str = '.logs',
        max_bytes: int = 524288,
        backup_count: int = 2,
        logger_name: str = __name__,
        msecs: bool = False,
    ) -> logging.Logger:
    
    loglevel = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITITCAL': logging.CRITICAL
    }
    mod = mods()
    
    try:
        level = loglevel[level.upper()]
    except (KeyError, AttributeError) as e:
        err_message = f'invalid level {e}: using default value "INFO"'
        level = logging.INFO
    else:
        err_message = None
    
    logdict = logging.root.manager.loggerDict
    if logger_name in logdict.keys():
        return logdict[logger_name]
    else:
        module_len = max_len()
        logger = logging.getLogger(logger_name)
        #logger.propagate = False
        logger.setLevel(level)
        asctime = '{asctime:15s}'
        #module = '{module:>10s}'
        module = '{:>{width}s}'.format('module', width=module_len)
        levelname = '#c{levelname:>8s}#r'
        message = '{message}'
        if msecs:
            _msecs = '.{msecs:03.0f}'
        else:
            _msecs = ''
        formatter = ColorFormatter(
            fmt=f'{asctime}{_msecs}| {mod.aqua(module)} {levelname}| {message}',
            datefmt='%Y-%m-%d %H:%M:%S',
            style='{'
   )    
        if not os.path.isdir(logdir): 
            os.mkdir(logdir)

        file_handler = RotatingFileHandler(
            f'{logdir}/{os.path.split(os.path.abspath("."))[-1]}.log',
            mode='a', maxBytes=max_bytes,
            backupCount=backup_count, encoding=None, 
            delay=0
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        if err_message is not None:
            logger.warning(
                f'{err_mesage}. level options: {list(loglevel.keys())}'
            )
        return logger

