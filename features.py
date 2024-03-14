"""
This file contains the features that helps for QA testing.
"""

import datetime

import os.path
import subprocess
import sys
import time

from rich.console import Console
from utilities import Errors, Commands, Checks, HandleFiles, NetworksOps
from webparser import WebParser


class Screenshot:

    def __init__(self):
        self.err = Errors()
        self.cmd = Commands()
        self.chk = Checks()
        self.hf = HandleFiles()
        self.home = os.path.expanduser('~')
        self.time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.wp = WebParser()
        self.console = Console()
        self.nops = NetworksOps()

    CHROME_UPLOAD_URL = "http://screen/"
    CHROME_WINDOW_WAIT_TIME = 10

    def takeScreenshot(self, name: str = None) -> str:
        if name is None:
            name = f"screenshot_{self.time}"
        else:
            name = name.replace(" ", "_")
        ss_path = f"/sdcard/{name}.png"
        dest_path = self.home
        self.cmd.runCommand(f'adb shell screencap {ss_path}')
        self.cmd.runCommand(f'adb pull {ss_path} {dest_path}')
        self.cmd.runCommand(f'adb shell rm {ss_path}')
        return os.path.join(self.home, f"{name}.png")

    def moveScreenshot(self, dest: str):
        self.hf.moveOrCopyFiles(['.png'], dest)

    def copy_and_upload_screenshot(self, img_path: str, is_upload: bool = False):
        try:
            if sys.platform == "darwin":
                try:
                    command = f'osascript -e "set the clipboard to (read \\"{img_path}\\" as TIFF picture)"'
                    self.cmd.runCommand(command)
                    if is_upload & self.nops.checkNetwork():
                        self.err.displayInfo(f'Waiting for chrome window to upload : {self.CHROME_WINDOW_WAIT_TIME} secs')
                        self.wp.openChrome(self.CHROME_UPLOAD_URL)
                        time.sleep(self.CHROME_WINDOW_WAIT_TIME)
                        cmd = 'osascript -e \'tell application "System Events" to keystroke "v" using command down\''
                        self.cmd.runSubprocess(cmd)
                        time.sleep(2)
                        self.err.displayInfo("If screenshot is not uploaded,"
                                             " just navigate to the window and paste it by command+v")
                        url_command = (f"osascript -e 'tell application \"Google Chrome\" to return URL of active tab "
                                       f"of front window as string'")
                        screenshot_url = self.cmd.runSubprocess(url_command)
                        self.console.print(f'Screenshot uploaded to {screenshot_url}')
                    self.err.displaySuccess('Done')
                except (Exception, subprocess.CalledProcessError):
                    self.err.displayError("Something went wrong in screenshot operations.")
                except KeyboardInterrupt:
                    self.err.displayInterrupt("Dude You interrupted me.... 😬")
            elif sys.platform == "linux":
                try:
                    command = f'xclip -selection clipboard -t image/png -i \\"{img_path}\\'
                    self.cmd.runCommand(command)
                    if is_upload & self.nops.checkNetwork():
                        result, out = self.cmd.runSubprocess(f'snipit -f {img_path}')
                        print(result)
                        if result != 0:
                            self.cmd.runSubprocess('sudo apt install snipit-cli')
                            res, output = self.cmd.runSubprocess(f'snipit -f {img_path}')
                            self.console.print(output)

                except (Exception, subprocess.CalledProcessError):
                    self.err.displayError("Something went wrong in screenshot operations.")
                except KeyboardInterrupt:
                    self.err.displayErrorExit("Dude You interrupted me.... 😬")
        except FileNotFoundError:
            self.err.displayError("File not found for copy or upload")

    def screenshot(self, is_upload: bool, name: str = None):
        self.moveScreenshot('screenshots')
        path = self.takeScreenshot(name)
        self.copy_and_upload_screenshot(img_path=path, is_upload=is_upload)


class Screenrecord:
    pass


if __name__ == "__main__":
    ss = Screenshot()
    ss.copy_and_upload_screenshot(img_path=ss.takeScreenshot(), is_upload=True)
