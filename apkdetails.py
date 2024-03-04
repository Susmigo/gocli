"""
This script manages the installed applications in the connected device
"""
import re

from devicedetails import DeviceDetails
from utilities import _run_command


class ApkDetails:

    @classmethod
    def _get_version(cls, package) -> str:
        version = _run_command(f"adb shell dumpsys package {package} | grep version")
        versionNamePattern = r'versionName=([^\s]*)'
        versionCodePattern = r'versionCode=([^\s]*)'
        versionName = re.findall(versionNamePattern, version)[0]
        versionCode = re.findall(versionCodePattern, version)[0]
        return f"{versionName} (versionCode={versionCode})"

    @classmethod
    def _version_printer(cls, packages) -> str:
        outString = ''
        for name, details in packages.items():
            package_name = name
            version_details = cls._get_version(f"{details['package']}")
            outString += f"{package_name} Version: {version_details}\n"
        return outString

    @classmethod
    def get_versions_from_experience(cls) -> str:
        amatiPackages = {'LauncherX': {'package': 'com.google.android.apps.tv.launcherx', 'version_details': None}}
        watsonPackages = {
            'TV Launcher': {'package': 'com.google.android.tvlauncher', 'version_details': None},
            'TV Recommendations': {'package': 'com.google.android.tvrecommendations', 'version_details': None}}
        commonPackages = {'GMS Core': {'package': 'com.google.android.gms', 'version_details': None},
                          'Play Store': {'package': "com.android.vending", 'version_details': None}}

        exp = DeviceDetails().get_experience()
        outString = ""
        if exp:
            outString += cls._version_printer(amatiPackages)
        else:
            outString += cls._version_printer(watsonPackages)

        outString += cls._version_printer(commonPackages)

        return outString

    @classmethod
    def final_print_str(cls) -> str:
        return cls.get_versions_from_experience()

    @classmethod
    def final_print_for_tabulate(cls) -> list:
        lines = cls.final_print_str().split('\n')
        result = [["**" + key.strip() + "**", value.strip()] for key, value in
                  (line.split(': ', 1) for line in lines if line)]
        return result


if __name__ == "__main__":
    print("For string:\n", ApkDetails.final_print_str())
    print("For tabulate:\n", ApkDetails.final_print_for_tabulate())
