import os.path
import subprocess
import sys
import time

from rich.console import Console
from datetime import datetime

from utils.checks import Checks
from utils.commands import Commands
from utils.display import Display
from utils.filehandler import FileHandler
from utils.network import NetworksOps
from webparser import WebParser


class Screenshot:

    def __init__(self):
        self.display = Display()
        self.cmd = Commands()
        self.chk = Checks()
        self.fh = FileHandler()
        self.home = os.path.expanduser('~')
        self.time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.wp = WebParser()
        self.console = Console()
        self.nops = NetworksOps()

    CHROME_UPLOAD_URL = "http://screen/"
    CHROME_WINDOW_WAIT_TIME = 10

    def takeScreenshot(self, name: str = None) -> str:
        if name is None:
            name = f"ss_{self.time}"
        else:
            name = name.replace(" ", "_")
        ss_path = f"/sdcard/{name}.png"
        dest_path = self.home
        self.cmd.adbCommand(f'adb shell screencap {ss_path}')
        self.cmd.adbCommand(f'adb pull {ss_path} {dest_path}')
        self.cmd.adbCommand(f'adb shell rm {ss_path}')
        return os.path.join(self.home, f"{name}.png")

    def moveScreenshot(self, dest: str):
        self.fh.moveOrCopyFiles(['.png'], destination=dest)

    def copy_and_upload_screenshot(self, img_path: str, is_upload: bool = False):
        try:
            if sys.platform == "darwin":
                try:
                    command = f'osascript -e "set the clipboard to (read \\"{img_path}\\" as TIFF picture)"'
                    self.cmd.adbCommand(command)
                    if is_upload & self.nops.checkNetwork():
                        self.display.info(
                            f'Waiting for chrome window to upload : {self.CHROME_WINDOW_WAIT_TIME} secs')
                        self.wp.openChrome(self.CHROME_UPLOAD_URL)
                        time.sleep(self.CHROME_WINDOW_WAIT_TIME)
                        cmd = 'osascript -e \'tell application "System Events" to keystroke "v" using command down\''
                        self.cmd.runSubprocess(cmd)
                        time.sleep(3)
                        self.display.info("If screenshot is not uploaded,"
                                          " just navigate to the window and paste it by command+v")
                        url_command = (f"osascript -e 'tell application \"Google Chrome\" to return URL of active tab "
                                       f"of front window as string'")
                        screenshot_url = self.cmd.runSubprocess(url_command)[1]
                        self.console.print(f'Screenshot uploaded to {screenshot_url}\n')
                    self.display.success('Done')

                except (Exception, subprocess.CalledProcessError) as e:
                    self.display.error("Something went wrong in screenshot operations.", trace=str(e))

                except KeyboardInterrupt:
                    self.display.interrupt("Dude You interrupted me.... 😬")

            elif sys.platform == "linux":
                try:
                    command = f'xclip -selection clipboard -t image/png -i \"{img_path}\"'
                    self.cmd.runSubprocess(command, timeout=1)
                    if is_upload & self.nops.checkNetwork():
                        result, out = self.cmd.runSubprocess(f'snipit -f {img_path}')
                        if result != 0:
                            self.cmd.runSubprocess('sudo apt install snipit-cli -y > /dev/null')
                            res, output = self.cmd.runSubprocess(f'snipit -f {img_path}')
                            self.console.print(output)
                        else:
                            self.console.print(out)
                        self.display.success("Done")

                except (Exception, subprocess.CalledProcessError) as e:
                    self.display.error(f"Something went wrong in screenshot operations.", trace=str(e))

                except KeyboardInterrupt:
                    self.display.interrupt("Dude You interrupted me.... 😬")

        except FileNotFoundError as e:
            self.display.error("File not found for copy or upload", trace=str(e))

    def screenshot(self, is_upload: bool, name: str = None):
        self.moveScreenshot('screenshots')
        path = self.takeScreenshot(name)
        self.copy_and_upload_screenshot(img_path=path, is_upload=is_upload)


if __name__ == "__main__":
    ss = Screenshot()
    ss.screenshot(is_upload=True, name="test")
