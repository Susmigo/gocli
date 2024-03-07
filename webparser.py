"""
This file opens the links in chrome.
"""
import platform
import subprocess
import urllib.parse

from utilities import displayErrorExit


class WebParser:
    __browserPaths = {
        'Darwin': "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        'Linux': "/opt/google/chrome/google-chrome"
    }

    @classmethod
    def __determinePlatform(cls) -> tuple[str, str]:
        return platform.system(), platform.machine()

    @classmethod
    def openChrome(cls, link: str):
        system, arch = cls.__determinePlatform()
        execPath = cls.__browserPaths.get(system, cls.__browserPaths['Linux'])
        args = ["--args", "--profile-directory=Default", link]
        try:
            command = [execPath] + args
            subprocess.Popen(command,stdout=subprocess.DEVNULL)
        except FileNotFoundError:
            displayErrorExit("Chrome executable path is not given correctly.")
        except Exception:
            displayErrorExit("Something went wrong.")

    @classmethod
    def descParser(cls, description: str) -> str:
        query = urllib.parse.quote(description)
        return query

    @classmethod
    def takeMetoBuganizer(cls, func):
        raw = cls.descParser(func)
        link = f"http://b/new?&description={raw}&format=MARKDOWN"
        cls.openChrome(link)


if __name__ == "__main__":
    WebParser.openChrome('b/')
    print(WebParser.descParser("helof sfhskfhs fskjfhskfh %% &24 & *q3467t 09093()"))
