"""
This file opens the links in chrome.
"""
import platform
import subprocess
import urllib.parse

from utilities import Errors, ChromeProfile


class WebParser:
    def __init__(self):
        self.err = Errors()
        self.cp = ChromeProfile()

    __browserPaths = {
        'Darwin': "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        'Linux': "/opt/google/chrome/google-chrome"
    }

    @staticmethod
    def __determinePlatform() -> tuple[str, str]:
        return platform.system(), platform.machine()

    def openChrome(self, link: str):
        system, arch = self.__determinePlatform()
        profile = self.cp.getProfileFromConfig()
        execPath = self.__browserPaths.get(system, self.__browserPaths['Linux'])
        args = ["--args", f"--profile-directory={profile}", link]
        try:
            command = [execPath] + args
            subprocess.Popen(command, stdout=subprocess.DEVNULL)
        except FileNotFoundError:
            self.err.displayErrorExit("Chrome executable path is not given correctly.")
        except Exception:
            self.err.displayErrorExit("Something went wrong.")

    @staticmethod
    def descParser(description: str) -> str:
        query = urllib.parse.quote(description)
        return query

    def takeMetoBuganizer(self, func):
        raw = self.descParser(func)
        link = f"http://b/new?&description={raw}&format=MARKDOWN"
        self.openChrome(link)


if __name__ == "__main__":
    wp = WebParser()
    wp.openChrome(link='b/')
    print(wp.descParser('jhsfwh 53w353453451@#$%^&8qr0'))
