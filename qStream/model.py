from . import MainWindow, Log2Signal, rtm_relay
from .styles import large as large_style
import os
import sys

import logging.handlers

from multiprocessing import Process, Queue, Event

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

class RTMstreamer(MainWindow):

    startSig = pyqtSignal()

    def dispatch(self, app, verbose=False, extra_callback=()):
        # to quit
        app.aboutToQuit.connect(self.on_quit)
        # prepare
        self.q = Queue()
        self.stop_event = Event()
        config_worker = {
            'version': 1,
            "formatters": {
                "simple": {
                    "format": "[%(levelname)s] %(message)s / %(name)s"
                    },
                },
            'handlers': {
                'queue': {
                    'class': 'logging.handlers.QueueHandler',
                    'queue': self.q,
                    },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    },
                },
            "loggers": {
                'RTM': {
                    'level': 'INFO',
                    "propagate": True if verbose else False,
                    'handlers': ["queue"],
                    },
                },
           "root": None,
            "disable_existing_loggers" : False,
            }
        if verbose>1:
            config_worker["root"] = {
               "level": "DEBUG",
               "handlers": ["console"]
                }
        # setup
        ## log to signal
        self.waiter = Log2Signal()
        self.waiter.new_message.connect(self.addChat1)
        ## trigger
        listener = logging.handlers.QueueListener(self.q,
                                                  self.waiter,
                                                  *extra_callback
                                                  )
        listener.start()
        ## message to log
        self.stream = Process(target=rtm_relay,
                              name="sc_RTM",
                              daemon=True,
                              args=(os.environ["SLACK_LEGACY_TOKEN"],
                                    self.stop_event,
                                    config_worker
                                    )
                              # config=config_worker
                              )
        # start
        self.stream.start()
        # need to be returned / app.exec_()

    def on_quit(self):
##        self.stream.disconnect()
        self.stop_event.set()
        self.stream.terminate()
        self.stream.join()

    @classmethod
    def go(cls, verbose=False, style=large_style, extra_callback=()):
        app = QApplication(sys.argv)
        app.setStyleSheet(style)
        me = cls()
        me.show()
        me.dispatch(app, verbose, extra_callback)
        logging.debug("===\n\n")
        sys.exit(app.exec_())

if __name__ == "__main__":
    pass
