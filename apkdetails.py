"""
This script manages the installed applications in the connected device
"""
import re

from devicedetails import DeviceDetails
from utilities import runCommand


class ApkDetails:

    @classmethod
    def getVersionNameCode(cls, package) -> str:
        version = runCommand(f"adb shell dumpsys package {package} | grep version")
        versionNamePattern = r'versionName=([^\s]*)'
        versionCodePattern = r'versionCode=([^\s]*)'
        versionName = re.findall(versionNamePattern, version)[0]
        versionCode = re.findall(versionCodePattern, version)[0]
        return f"{versionName} (versionCode={versionCode})"

    @classmethod
    def versionPrinter(cls, packages) -> str:
        _outString = ''
        for name, details in packages.items():
            package_name = name
            version_details = cls.getVersionNameCode(f"{details['package']}")
            _outString += f"{package_name} Version: {version_details}\n"
        return _outString

    @classmethod
    def getVersionsFromExperience(cls) -> str:
        amatiPackages = {'LauncherX': {'package': 'com.google.android.apps.tv.launcherx', 'version_details': None}}
        watsonPackages = {'TV Launcher': {'package': 'com.google.android.tvlauncher', 'version_details': None},
            'TV Recommendations': {'package': 'com.google.android.tvrecommendations', 'version_details': None}}
        commonPackages = {'GMS Core': {'package': 'com.google.android.gms', 'version_details': None},
                          'Play Store': {'package': "com.android.vending", 'version_details': None}}

        _exp = DeviceDetails().getExperience()
        _outString = ""
        if _exp:
            _outString += cls.versionPrinter(amatiPackages)
        else:
            _outString += cls.versionPrinter(watsonPackages)

        _outString += cls.versionPrinter(commonPackages)

        return _outString

    @classmethod
    def finalPrint(cls) -> str:
        return cls.getVersionsFromExperience()

    @classmethod
    def finalPrintTabulate(cls) -> list:
        _lines = cls.finalPrint().split('\n')
        _result = [["**" + _key.strip() + "**", _value.strip()] for _key, _value in
                   (_line.split(': ', 1) for _line in _lines if _line)]
        return _result


if __name__ == "__main__":
    print("For string:\n", ApkDetails.finalPrint())
    print("For tabulate:\n", ApkDetails.finalPrint())
