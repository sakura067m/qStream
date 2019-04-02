import os
import sys
import time
import logging
import logging.config
from slackclient import SlackClient

from PyQt5.QtCore import pyqtSignal, QObject


class Log2Signal(QObject):

    new_message = pyqtSignal(str)

    def handle(self, record):
        self.new_message.emit(record.getMessage())

def logRTM(token, stop_event, config):
    logging.config.dictConfig(config)
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]
    logger = logging.getLogger("RTM")

    # setup slack client
    sc = SlackClient(token)

    if sc.rtm_connect():
        while not stop_event.is_set() and sc.server.connected is True:
            rtm_response = sc.rtm_read()
            for message in rtm_response:
##                print(message)
                if "subtype" in message: continue
                message_type = message["type"]
                if "message" == message_type:
                    logger.info(message["text"])
                else:
                    pass
            time.sleep(1)
        print("closing")
    else:
        print("Connection Failed")
