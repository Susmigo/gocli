"""
This file gives the Bug description based on the user input.
"""

from tabulate import tabulate

from accounts import Accounts
from apkdetails import ApkDetails
from devicedetails import DeviceDetails


class TableFormatter:
    @classmethod
    def bugTableFormatter(cls, fmt: str = "pipe"):
        headers = ['Environment', ' Details']
        table = []
        table.extend(DeviceDetails().finalPrintTabulate())
        table.extend(ApkDetails().finalPrintTabulate())
        table.extend(Accounts().finalPrintTabulate())
        return tabulate(table, headers, tablefmt=fmt)

    @classmethod
    def commentTableFormatter(cls) -> str:
        _output = (f"{DeviceDetails.finalPrint()}\n"
                   f"{ApkDetails.finalPrint()}"
                   f"{Accounts.finalPrint()}")
        return _output.strip()


class Descriptor:

    @classmethod
    def bugDescriptor(cls):
        launcherxText = (f"1. Setup the device with **{DeviceDetails.getLocale()}** locale and install the above "
                         f"LauncherX build.")
        watsonText = (f"1. Setup the device with **{DeviceDetails.getLocale()}** locale and install the above TV Home "
                      f"and TV Core builds.")
        _output = (f"\n##### TEST ENVIRONMENT:\n"
                   f"{TableFormatter.bugTableFormatter()}\n\n"
                   f"NOTE: Please change the component if it is not relevant.\n\n"
                   f"##### STEPS TO REPRODUCE:\n"
                   f"{launcherxText if DeviceDetails.getExperience() else watsonText}\n"
                   f"2. Connect to the **`US`** region using a VPN.\n3.\n4.\n\n"
                   f"##### EXPECTED RESULT:\n- \n\n"
                   f"##### OBSERVED RESULT:\n- \n\n"
                   f"##### REPRO RATE: 5/5\n\n"
                   f"##### SCREEN RECORDING:\n- \n\n"
                   f"##### SHERLOGS:\n-\n\n"
                   f"##### LOGS:\n-\n\n"
                   f"Attached Bugreport and Screen Recording.")
        return _output

    @classmethod
    def commentDescriptor(cls):
        _output = (f"The issue is reproducible,\n\n"
                   f"Tested in following environment:\n"
                   f"##### Test Environment:\n"
                   f"````\n"
                   f"{TableFormatter.commentTableFormatter()}\n"
                   f"````\n"
                   f"##### Screen Recording:\n-\n"
                   f"##### Sherlogs:\n-\n"
                   f"Attached Bugreport and Screen recording.")
        return _output


if __name__ == "__main__":
    # print(TableFormatter.bugTableFormatter())
    # print(TableFormatter.commentTableFormatter())
    # print(Descriptor.commentDescriptor())
    print(Descriptor.bugDescriptor())
