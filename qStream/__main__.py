from . import *
import os
import sys

import logging.handlers

from multiprocessing import Process, Queue, Event

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

class RTMstreamer(MainWindow):

    startSig = pyqtSignal()

    def dispatch(self, app):
        # to quit
        app.aboutToQuit.connect(self.on_quit)
        # prepare
        self.q = Queue()
        self.stop_event = Event()
        config_worker = {
            'version': 1,
            # 'disable_existing_loggers': True,
            'handlers': {
                'queue': {
                    'class': 'logging.handlers.QueueHandler',
                    'queue': self.q,
                },
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['queue']
            },

            }
        # setup
        ## log to signal
        self.waiter = Log2Signal()
        self.waiter.new_message.connect(self.addChat1)
        ## trigger
        listener = logging.handlers.QueueListener(self.q, self.waiter)
        listener.start()
        ## message to log
        self.stream = Process(target=logRTM,
                              name="sc_RTM",
                              daemon=True,
                              args=(os.environ["SLACK_LEGACY_TOKEN"],
                                    self.stop_event,
                                    config_worker
                                    )
                              )
        # start
        self.stream.start()

    def on_quit(self):
##        self.stream.disconnect()
        self.stop_event.set()
        self.stream.join()
        self.stream.terminate()

    @classmethod
    def go(cls, style=default_style):
        app = QApplication(sys.argv)
        app.setStyleSheet(style)
        me = cls()
        me.show()
        me.dispatch(app)
        print("===\n\n")
        sys.exit(app.exec_())



if __name__ == "__main__":
    print("poo")
    if "darwin" == sys.platform:
        import multiprocessing as mp
        mp.set_start_method("spawn")
    RTMstreamer.go()
