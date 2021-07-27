from __future__ import unicode_literals

import logging


logger = logging.getLogger("Survey")
NOTIFY = 35


class Logger:
    """
    Logger
    """

    @staticmethod
    def info(stream):
        """info"""
        logger.info(stream)

    @staticmethod
    def warning(stream):
        """warning logs"""
        logger.warning(stream)

    @staticmethod
    def error(stream):
        """error logs"""
        logger.error(stream)

    @staticmethod
    def notify(stream):
        """Custom Log Level"""
        logger.log(NOTIFY, stream)
