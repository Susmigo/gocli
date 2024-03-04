"""
This Script gives the version and version code of the installed applications
"""
import re

import requests
from bs4 import BeautifulSoup
from google_play_scraper import app, exceptions
from tabulate import tabulate

from utilities import _run_command


class VersionMangager:
    @classmethod
    def listpackages(cls) -> list[str]:
        raw = _run_command('adb shell pm list packages').split('\n')
        packageslist = [(pckg.split(':', 1)[1]) for pckg in raw]
        return packageslist

    @classmethod
    def getversionname(cls, _package: str) -> str:
        packageversionname = _run_command(f'adb shell dumpsys package {_package} | grep versionName=').split('\n', 1)
        return packageversionname[0].split('=', 1)[1]

    @classmethod
    def getversioncode(cls, _package: str) -> str:
        packageversioncode = _run_command(f'adb shell dumpsys package {_package} | grep versionCode=').split('\n', 1)
        return packageversioncode[0].split(' ', 1)[0]

    @classmethod
    def getversionnamecode(cls, _package) -> str:
        version = _run_command(f"adb shell dumpsys package {_package} | grep version")
        versionNamePattern = r'versionName=([^\s]*)'
        versionCodePattern = r'versionCode=([^\s]*)'
        versionName = re.findall(versionNamePattern, version)[0]
        versionCode = re.findall(versionCodePattern, version)[0]
        return f"{versionName} (versionCode={versionCode})"

    @classmethod
    def final_print_for_tabulate(cls) -> list:
        res = ""
        for _ in cls.listpackages():
            res += f"{PlaystoreScrapper.getappname(_)}* {_}* {cls.getversionnamecode(_)}\n"
        table_data = res.split('\n')
        return [[title.strip(), package.strip(), version.strip()]
                for title, package, version in [(line.split('* ', 2)) for line in table_data if line]]


class PlaystoreScrapper:

    @classmethod
    def getappname(cls, package: str) -> str:
        try:
            appname = app(package)
        except exceptions.NotFoundError:
            appname = {'title': 'System app'}
        return appname['title']

    @classmethod
    def getversion(cls, package: str):
        try:
            appversion = app(package)
        except exceptions.NotFoundError:
            appversion = {'version': 'Not found'}
        return appversion

    @classmethod
    def getpackagetitles(cls):
        packages = VersionMangager.listpackages()
        for _ in packages:
            print(_, cls.getappname(_))


class Test:

    @classmethod
    def getappname(cls, package: str):
        playurl = f"https://play.google.com/store/apps/details?id={package}"
        r = requests.get(playurl)
        soup = BeautifulSoup(r.content, 'html.parser')
        output = soup.text.split(' - A')[0] if not soup.text.split(' - A')[0].count("We're sorry") else "System App"
        return {'title': output, 'package': package,
                'version': VersionMangager.getversionnamecode(package), 'url': r.url}

    @classmethod
    def runner(cls):
        pkg = VersionMangager.listpackages()
        relist = []
        headers = ['App Name', 'Package', 'Version (code)', 'Play Url']
        for _ in sorted(pkg):
            relist.append(list(Test.getappname(_).values()))
        print(tabulate(headers=headers, tabular_data=relist, tablefmt="pipe", ))


if __name__ == "__main__":
    pkg = VersionMangager.listpackages()
    relist = []
    headers = ['App Name', 'Package', 'Version (code)', 'Play Url']
    for _ in sorted(pkg):
        relist.append(list(Test.getappname(_).values()))
    print(tabulate(headers=headers, tabular_data=relist, tablefmt="pipe",))
