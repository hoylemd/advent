import os
import logging
import fileinput

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
logger.addHandler(ch)


def parse_input():
    return (line.strip() for line in fileinput.input())
