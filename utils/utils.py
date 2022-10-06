import logging
from typing import Optional

import yaml


def logging_setup(mod_name: str, debug: bool = False) -> logging.Logger:
    """
    Setup for logging with some formatting I enjoy.
    Can set to be in debug mode, will edit messages to convey the same.
    :param mod_name: module name to reference with
    :param debug: if True, switch to debug level
    :return: logger object to use throughout
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s :: %(levelname)s :: %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if debug:
        formatter_debug = logging.Formatter(
            'DEBUG_MODE :: %(asctime)s %(name)-12s :: %(levelname)s :: %(message)s'
        )
        handler.setFormatter(formatter_debug)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger
    return logger


def get_config(loc: Optional[str] = None) -> dict:
    """
    Loads in-project config file, optional filelocation can be passed as well.
    :param loc: [OPTIONAL] file location
    :return: dict of yaml data
    """
    with open(loc if loc else 'config.yml') as f:
        return yaml.safe_load(f)