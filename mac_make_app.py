import sys
import os
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QLabel
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

# save_button = QMessageBox.Save
# cancel_button = QMessageBox.Cancel
# help_button = QMessageBox.Help

app = QApplication(sys.argv)
url_token = QUrl("https://api.slack.com/custom-integrations/legacy-tokens")
text_question = """\
Do you want to save the token?
To open your browzer to get the token, push \"Help\".
"""
buttons_question = QMessageBox.Save|QMessageBox.No|QMessageBox.Help|QMessageBox.Abort

while True:
    do_process = QMessageBox.question(None,
                                      "SLACK_LEGACY_TOKEN",
                                      text_question,
                                      buttons_question,
                                      QMessageBox.Abort,
                                      )
    if QMessageBox.No == do_process:
        break
    if QMessageBox.Help == do_process:
        QDesktopServices.openUrl(url_token)
        continue
    if QMessageBox.Abort == do_process:
        is_exit = QMessageBox.warning(None,
                                      "",
                                      "Are you going to abort?",
                                      QMessageBox.Yes,
                                      QMessageBox.No,
                                      )
        if QMessageBox.Yes == is_exit:
            sys.exit("Aborted!")
        else:
            continue

    token, ok =  QInputDialog.getText(None, "Save token", "Input the token")
    if not ok:
        continue
    else:
        break

#start making app

import shutil
try:
    shutil.copytree("./qStream.app", "/Applications/qStream.app")
except FileExistsError:
    print("qStream App is already exists.")
sh_dst = "/Applications/qStream.app/Contents/MacOS/script.sh"
with open(sh_dst, "w") as f:
    if QMessageBox.No == do_process:
        print("Preparing a script without token.")
        f.write("#!/bin/sh\nqStream --css large\n")
    else:
        print("Preparing a script.")
        f.write("""\
#!/bin/sh
export SLACK_LEGACY_TOKEN={}
qStream --css large)
""".format(token))

os.chmod(sh_dst,0o774)

print("Setup done.")
