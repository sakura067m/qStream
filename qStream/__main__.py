from . import RTMstreamer
import os
import sys

def main():
    if "SLACK_LEGACY_TOKEN" not in os.environ:
        print("""\
SLACK_LEGACY_TOKEN didn't found in os.environ.
Please get the token and set it as SLACK_LEGACY_TOKEN.
We will recommend;
*** in your CLI
SLACK_LEGACY_TOKEN=<your token here> python -m qStream
***
Also, you can set it by;
*** in some setting file
export SLACK_LEGACY_TOKEN=<your token here>
***

For the further information, see https://github.com/sakura067m/qStream
"""
        )
        from PyQt5.QtWodgets import QApplication, QMessageBox
        app = QApplication(sys.argv)
        QMessageBox.warning(None,
                            "missing a token",
                            "please set the token",
                            QMessageBox.Yes,
                            QMessageBox.Yes
                            )

        raise KeyError("SLACK_LEGACY_TOKEN")
    if "darwin" == sys.platform:
        import multiprocessing as mp
        mp.set_start_method("spawn")
    if 1 >= len(sys.argv):
        RTMstreamer.go()
    else:
        import argparse
        import fileinput
        from io import StringIO

        parser = argparse.ArgumentParser(
            prog="python -m qStream",
            description="Stream message from slack",
            epilog="Homepage: https://github.com/sakura067m/qStream",
            )
        # parser.add_argument("-f", action="store_true")
        css_group = parser.add_mutually_exclusive_group()
        css_group.add_argument("--css", metavar="style",
                               choices=["mini", "large"],
                               help="use built-in style",
                               )
        css_group.add_argument("-f", metavar="CSS", nargs="*",
                            help="CSS for app's style sheet",
                            )
        parser.add_argument("-v", "--verbose", action="count",
                            default=False,
                            help="show messages in CLI too",
                            )
        args = parser.parse_args()

        if args.css:
            from . import styles
            s = getattr(styles,args.css)
        elif None is args.f:
            s = None
        else:
            buf = StringIO()
            with fileinput.input(files=args.files) as f:
                for l in f:
                    buf.write(l)
            s = buf.getvalue()
            buf.close()

        if s:
            # start streaming with a css from input
            RTMstreamer.go(verbose=args.verbose,style=s)
        else:
            RTMstreamer.go(verbose=args.verbose)

if __name__ == "__main__":
    main()
