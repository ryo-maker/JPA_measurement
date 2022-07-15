"""logging_utilityはloggerを作成するモジュールです. / This is a module that 
creates a logger.


Available functions
-------------------
get_normal_logger
    handlerとしてStreamHandlerのみ使用するloggerを返す. / Return a logger that 
    uses only StreamHandler as handler.

get_file_output_logger
    handlerとしてStreamHandlerとFileHandlerを使用するloggerを返す. / Return a 
    logger that uses StreamHandler and FileHandler as handler.

kill_loggers
    loggerを全て消去する. / Clear all loggers.
"""


import os
from logging import StreamHandler, FileHandler, Formatter, getLogger, shutdown
from utility import CURRENT_PATH
from utility.constants import LOGGING_LEVEL_DICT
from utility.others import get_time


__all__ = [
    "get_normal_logger",
    "get_file_output_logger",
    "kill_loggers",
]
__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "1.11.0"
__date__ = "2022/03/08"


"""The Formatter can be initialized with a format string which makes use of 
knowledge of the LogRecord attributes - e.g. the default value mentioned above 
makes use of the fact that the user"s message and arguments are pre-formatted 
into a LogRecord"s message attribute. Currently, the useful attributes in a 
LogRecord are described by:
%(name)s            - Name of the logger (logging channel)
%(levelno)s         - Numeric logging level for the message 
                      (DEBUG, INFO, WARNING, ERROR, CRITICAL)
%(levelname)s       - Text logging level for the message 
                      ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
%(pathname)s        - Full pathname of the source file where the logging call 
                      was issued (if available)
%(filename)s        - Filename portion of pathname
%(module)s          - Module (name portion of filename)
%(lineno)d          - Source line number where the logging call was issued 
                      (if available)
%(funcName)s        - Function name
%(created)f         - Time when the LogRecord was created (time.time() return value)
%(asctime)s         - Textual time when the LogRecord was created
%(msecs)d           - Millisecond portion of the creation time
%(relativeCreated)d - Time in milliseconds when the LogRecord was created, 
                      relative to the time the logging module was loaded 
                      (typically at application startup time)
%(thread)d          - Thread ID (if available)
%(threadName)s      - Thread name (if available)
%(process)d         - Process ID (if available)
%(message)s         - The result of record.getMessage(), computed just as the 
                      record is emitted
"""
DEFAULT_FORMATTER_STRING = (
    "[ %(asctime)s | "
    "%(module)s | "
    "%(funcName)s | "
    "%(levelname)s ] "
    "%(message)s"
)


loggers = {}


def get_normal_logger(
    logger_name=__name__, format_string=DEFAULT_FORMATTER_STRING, level="debug"
):
    """handlerとしてStreamHandlerのみ使用するloggerを返す. / Return a logger that 
    uses only StreamHandler as handler.

    Parameters
    ----------
    logger_name : str, default: __name__
        ロガーの名前 / name of logger
    format_string : str, default: DEFAULT_FORMATTER_STRING
        フォーマット文字列 / format string
    level : str, default: "debug"
        ログレベル / level of logger

    Returns
    -------
    logging.Logger
        ロガー
    """
    stream_handler = StreamHandler()
    stream_handler.setFormatter(Formatter(fmt=format_string))
    stream_handler.setLevel(LOGGING_LEVEL_DICT[level])
    logger = getLogger(logger_name)
    logger.setLevel(LOGGING_LEVEL_DICT[level])
    logger.addHandler(stream_handler)
    logger.propagate = False
    loggers[logger_name] = logger
    return logger


def get_file_output_logger(
    logger_name=__name__,
    format_string=DEFAULT_FORMATTER_STRING,
    log_file_path=CURRENT_PATH,
    log_file_name=get_time(),
    level="debug",
):
    """handlerとしてStreamHandlerとFileHandlerを使用するloggerを返す. / Return a 
    logger that uses StreamHandler and FileHandler as handler.

    Parameters
    ----------
    logger_name : str, default: __name__
        ロガーの名前 / name of logger
    format_string : str, default: DEFAULT_FORMATTER_STRING
        フォーマット文字列 / format string
    log_file_path : str, default: os.getcwd()
        ログを記録するファイルのパス / path of the file to log
    log_file_name : str, default: utility.others.get_time()
        ログを記録するファイルの名前 / name of the file to log
    level : str, default: "debug"
        ログレベル / lovel of logger

    Returns
    -------
    logging.Logger
        ロガー
    """
    os.makedirs(log_file_path, exist_ok=True)
    formatter = Formatter(fmt=format_string)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(LOGGING_LEVEL_DICT[level])
    file_handler = FileHandler(log_file_path + "/" + log_file_name + ".log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(LOGGING_LEVEL_DICT[level])
    logger = getLogger(logger_name)
    logger.setLevel(LOGGING_LEVEL_DICT[level])
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    loggers[logger_name] = logger
    return logger


def kill_loggers():
    """loggerを全て消去する. / Clear all loggers."""
    for element_of_loggers in loggers:
        logger = loggers.get(element_of_loggers)
        for element_ofhandlers in logger.handlers:
            logger.removeHandler(element_ofhandlers)
    shutdown()
