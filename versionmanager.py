"""
This Script gives the version and version code of the installed applications
"""
import re

import httpx
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from utilities import Commands


class VersionManager:
    def __init__(self):
        self.cmd = Commands()
        self.vm = VersionManager()
        self.ps = PlayStoreScrapper()

    def listPackages(self) -> list[str]:
        _raw = self.cmd.runCommand('adb shell pm list packages').split('\n')
        return [(pckg.split(':', 1)[1]) for pckg in _raw]

    def getVersionName(self, _package: str) -> str:
        _packageversionname = self.cmd.runCommand(f'adb shell dumpsys package {_package} | grep versionName=').split(
            '\n', 1)
        return _packageversionname[0].split('=', 1)[1]

    def getVersionCode(self, _package: str) -> str:
        _packageversioncode = self.cmd.runCommand(f'adb shell dumpsys package {_package} | grep versionCode=').split(
            '\n', 1)
        return _packageversioncode[0].split(' ', 1)[0]

    def getVersionNameCode(self, _package) -> str:
        version = self.cmd.runCommand(f"adb shell dumpsys package {_package} | grep version")
        versionNamePattern = r'versionName=([^\s]*)'
        versionCodePattern = r'versionCode=([^\s]*)'
        versionName = re.findall(versionNamePattern, version)[0]
        versionCode = re.findall(versionCodePattern, version)[0]
        return f"{versionName} (versionCode={versionCode})"

    def finalPrintTabulate(self) -> list:
        res = ""
        for _ in self.listPackages():
            res += f"{self.ps.get_app_name(_)}* {_}* {self.getVersionNameCode(_)}\n"
        table_data = res.split('\n')
        return [[title.strip(), package.strip(), version.strip()]
                for title, package, version in [(line.split('* ', 2)) for line in table_data if line]]


# class PlaystoreScrapper:
#
#     @classmethod
#     def getappname(cls, package: str) -> str:
#         try:
#             appname = app(package)
#         except exceptions.NotFoundError:
#             appname = {'title': 'System app'}
#         return appname['title']
#
#     @classmethod
#     def getversion(cls, package: str):
#         try:
#             appversion = app(package)
#         except exceptions.NotFoundError:
#             appversion = {'version': 'Not found'}
#         return appversion
#
#     @classmethod
#     def getpackagetitles(cls):
#         packages = VersionMangager.listpackages()
#         for _ in packages:
#             print(_, cls.getappname(_))


class PlayStoreScrapper:

    def __init__(self):
        self.vm = VersionManager()

    def getappname(self, package: str):
        playurl = f"https://play.google.com/store/apps/details?id={package}"
        r = requests.get(playurl)
        soup = BeautifulSoup(r.content, 'html.parser')
        output = soup.text.split(' - A')[0] if not soup.text.split(' - A')[0].count("We're sorry") else "System App"
        return {'title': output, 'package': package,
                'version': self.vm.getVersionNameCode(package), 'url': r.url}

    async def get_app_name(self, package: str):
        play_url = f"https://play.google.com/store/apps/details?id={package}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(play_url)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                title_prefix = ' - A'
                output = (
                    soup.text.split(title_prefix)[0]
                    if not soup.text.split(title_prefix)[0].count("We're sorry")
                    else "System App"
                )

                return {
                    'title': output,
                    'package': package,
                    'version': await self.vm.getVersionNameCode(package),
                    'url': response.url
                }

            except httpx.RequestError as e:
                print(f"Error during request: {e}")
                return None


if __name__ == "__main__":
    vm = VersionManager()
    pkg = vm.listPackages()
    relist = []
    headers = ['App Name', 'Package', 'Version (code)', 'Play Url']
    # for _ in sorted(pkg):
    #     relist.append(list(PlayStoreScrapper.getappname(_).values()))
    print(tabulate(headers=headers, tabular_data=vm.finalPrintTabulate(), tablefmt="pipe", ))
