import logging
from config import *


def x_ss_bs():
    """
    Calculation of suspended solids concentration in
    the bottom sludge
    :return: FLOAT result in g/L or kg/m³
    """
    return ((1000
            / np.mean(SVI["Favourable"]["Nitrification and denitrification"]))
            * TTH["Thickening time"]
            ["Activated sludge plants with denitrification"][0] ** (1 / 3))


def x_ss_rs(using="scraper facilities"):
    """
    Calculation of suspended solids concentration in the return
    sludge using scraper facilities
    :param using: STRING indicating the type of facility to be used
    :return: FLOAT result in g/L or kg/m³
    """
    if using == "scraper facilities":
        return 0.7 * x_ss_bs()
    elif using == "suction facilities":
        return 0.6 * x_ss_bs()


def calc_weights(start, end, variable):
    """
    Calculation of initial and final weights of the dimensioning
    sludge age
    :param start: INT of the starting value in one of the sludge
    age ranges
    :param end: INT of the ending value in one of the sludge age
    ranges
    :param variable: FLOAT of the variable to be found its weights
    :return: TUPLE with dimensionless FLOATS results
    """
    start_weight = (end - variable) / (end - start)
    end_weight = 1 - start_weight
    return start_weight, end_weight


def start_logging():
    """
    To set up logging formats and log file names for different scenarios
    :return: None, but three logger objects will be created
    """
    loggers_config = {
        "info_logger": {"level": logging.INFO, "filename": "info.log",
                        "format": "[%(asctime)s] %(message)s"},
        "warning_logger": {
            "level": logging.WARNING, "filename": "warning.log",
            "format": "[%(asctime)s %(levelname)s: %(message)s"
        },
        "error_logger": {"level": logging.ERROR, "filename": "error.log",
                         "format": "[%(asctime)s %(levelname)s: %(message)s"}
    }
    for logger_key, logger_value in loggers_config.items():
        logger = logging.getLogger(logger_key)
        logger.setLevel(logger_value["level"])
        # file handler for log file
        file_handler = logging.FileHandler(logger_value["filename"], mode="w")
        file_handler.setFormatter(logging.Formatter(logger_value["format"]))
        logger.addHandler(file_handler)
        # stream handler for terminal output
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(logger_value["format"]))
        logger.addHandler(stream_handler)


def log_actions(fun):
    """
    'log_actions' decorator
    :param fun: a function
    :return: result of applying the wrapper function to the
    corresponding "fun"
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function in order to log script execution messages
        :param args: optional arguments
        :param kwargs: optional keyword arguments
        :return: None
        """
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()
    return wrapper
