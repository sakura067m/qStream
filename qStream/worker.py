import os
import sys
import time
from multiprocessing import Process
import logging
import logging.config
from slack import RTMClient

from PyQt5.QtCore import pyqtSignal, QObject

rtmLogger = logging.getLogger("RTM")

class Log2Signal(QObject):

    new_message = pyqtSignal(str)

    def handle(self, record):
        self.new_message.emit(record.getMessage())

@RTMClient.run_on(event="message")
def logRTM(**payload):
    message = payload["data"]
    if "subtype" in message: return
    rtmLogger.info(message["text"])

def rtm_relay(token, stop_event, config):
    logging.config.dictConfig(config)
    rtmLogger.debug("start relay")
    # setup slack client
    sc = RTMClient(token=token)
    sc.start()  # start async loop

if __name__ == "__main__":
    # slack_token = os.environ["SLACK_LEGACY_TOKEN"]
    # rtm_client = RTMClient(token=slack_token)
    pass
