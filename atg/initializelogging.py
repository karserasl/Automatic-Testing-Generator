# @Author: Lampros.Karseras
# @Date:   01/12/2020 11:13
import logging
import socket


def setUpLogging():
    format = f'%(asctime)s {socket.gethostname()} [%(process)d:%(thread)d]: %(levelname)s:%(name)s:%(message)s'

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # ensuring logging messages will be send to handlers
    handler = logging.StreamHandler()
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def initializeLogging():
    setUpLogging()
