"""
This script manages the installed applications in the connected device.
"""
import re

from devicedetails import DeviceDetails
from utils.checks import Checks
from utils.commands import Commands
from utils.display import Display


class ApkDetails:
    def __init__(self):
        self.cmd = Commands()
        self.chk = Checks()
        self.display = Display()
        self.dut = DeviceDetails()

    def getVersionNameCode(self, package) -> str:
        # noinspection PyCompatibility
        version = self.cmd.adbCommand(f"adb shell dumpsys package {package} | grep version")
        versionNamePattern = r'versionName=([^\s]*)'
        versionCodePattern = r'versionCode=([^\s]*)'
        versionName = re.findall(versionNamePattern, version)[0]
        versionCode = re.findall(versionCodePattern, version)[0]
        return f"{versionName} (versionCode={versionCode})"

    def versionPrinter(self, packages) -> str:
        _outString = ''
        for name, details in packages.items():
            package_name = name
            version_details = self.getVersionNameCode(f"{details['package']}")
            _outString += f"{package_name} Version: {version_details}\n"
        return _outString

    def getVersionsFromExperience(self) -> str:
        amatiPackages = {'LauncherX': {'package': 'com.google.android.apps.tv.launcherx', 'version_details': None}}
        watsonPackages = {'TV Launcher': {'package': 'com.google.android.tvlauncher', 'version_details': None},
                          'TV Recommendations': {'package': 'com.google.android.tvrecommendations',
                                                 'version_details': None}}
        commonPackages = {'GMS Core': {'package': 'com.google.android.gms', 'version_details': None},
                          'Play Store': {'package': "com.android.vending", 'version_details': None}}

        _exp = self.dut.getExperience()
        _outString = ""
        if _exp:
            _outString += self.versionPrinter(amatiPackages)
        else:
            _outString += self.versionPrinter(watsonPackages)

        _outString += self.versionPrinter(commonPackages)

        return _outString

    def finalPrint(self) -> str:
        return self.getVersionsFromExperience()

    def finalPrintTabulate(self) -> list:
        _lines = self.finalPrint().split('\n')
        _result = [["**" + _key.strip() + "**", _value.strip()] for _key, _value in
                   (_line.split(': ', 1) for _line in _lines if _line)]
        return _result


if __name__ == "__main__":
    apkDetails = ApkDetails()
    print("For string:\n", apkDetails.finalPrint())
    print("For tabulate:\n", apkDetails.finalPrintTabulate())
