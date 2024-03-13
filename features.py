"""
This file contains the features that helps for QA testing.
"""

import datetime

import os.path
import pyautogui
import sys
import time

from rich.console import Console
from utilities import Errors, Commands, Checks, HandleFiles
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
                    if is_upload:
                        self.err.displayInfo('Waiting for chrome window to upload : 10 secs\n')
                        self.wp.openChrome('http://screen/')
                        time.sleep(10)
                        cmd = 'osascript -e \'tell application "System Events" to keystroke "v" using command down\''
                        self.cmd.runCommand(cmd)
                        time.sleep(2)
                        self.err.displayInfo("If screenshot is not uploaded,"
                                             " just navigate to the window and paste it by command+v")
                        self.console.print('Screenshot uploaded to screen/')
                    self.err.displaySuccess('Done')
                except Exception:
                    self.err.displayError("Something went wrong in screenshot operations.")
            else:
                if sys.platform == "linux":
                    try:
                        command = f'xclip -selection clipboard -t image/png -i \\"{img_path}\\'
                        self.cmd.runCommand(command)
                        if is_upload:
                            self.err.displayInfo('Waiting for chrome window to upload : 10 secs\n')
                            self.wp.openChrome('http://screen/')
                            time.sleep(10)
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(2)
                            self.console.print('Screenshot uploaded to screen/')
                    except Exception:
                        self.err.displayError("Something went wrong in screenshot operations.")
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
    ss.copy_and_upload_screenshot(is_upload=True)
