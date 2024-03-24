"""
This file gives the Bug description based on the user input.
"""

from tabulate import tabulate

from accounts import Accounts
from apkdetails import ApkDetails
from devicedetails import DeviceDetails


class TableFormatter:

    def __init__(self):
        """
        Base class for table formatter.
        """
        self.acc = Accounts()
        self.apk = ApkDetails()
        self.dut = DeviceDetails()

    def bug_table_formatter(self, fmt: str = "pipe"):
        """
        Gives the format for bug table.
        """
        headers = ['Environment', ' Details']
        table = []
        table.extend(self.dut.finalPrintTabulate())
        table.extend(self.apk.finalPrintTabulate())
        table.extend(self.acc.final_print_tabulate())
        return tabulate(table, headers, tablefmt=fmt)

    def comment_table_formatter(self) -> str:
        """
        Gives the table format for comment.
        """
        _output = (f"{self.dut.finalPrint()}\n"
                   f"{self.apk.finalPrint()}"
                   f"{self.acc.final_print()}")
        return _output.strip()


class Descriptor(TableFormatter):

    def __init__(self):
        super().__init__()

    def bug_descriptor(self):
        """
        Generates the Bug description.
        """
        device_locale = self.dut.getLocale()
        locale = device_locale if device_locale is not None else "en-US"  # if the device locale returns none.
        launcherXText = (f"1. Setup the device with **{locale}** locale and install the above "
                         f"LauncherX build.")
        watsonText = (f"1. Setup the device with **{locale}** locale and install the above TV Home "
                      f"and TV Core builds.")
        _output = (f"\n##### TEST ENVIRONMENT:\n"
                   f"{self.bug_table_formatter()}\n\n"
                   f"NOTE: Please change the component if it is not relevant.\n\n"
                   f"##### STEPS TO REPRODUCE:\n"
                   f"{launcherXText if self.dut.getExperience() else watsonText}\n"
                   f"2. Connect to the **{locale.split('-',1)[1]}** region using a VPN.\n3.\n4.\n\n"
                   f"##### EXPECTED RESULT:\n- \n\n"
                   f"##### OBSERVED RESULT:\n- \n\n"
                   f"##### REPRO RATE: 5/5\n\n"
                   f"##### SCREEN RECORDING:\n- \n\n"
                   f"##### SHERLOGS:\n-\n\n"
                   f"##### LOGS:\n-\n\n"
                   f"Attached Bugreport and Screen Recording.")
        return _output

    def comment_descriptor(self):
        """
        Generates the Comment Description.
        """
        _output = (f"The issue is reproducible,\n\n"
                   f"Tested in following environment:\n"
                   f"##### Test Environment:\n"
                   f"````\n"
                   f"{self.comment_table_formatter()}\n"
                   f"````\n"
                   f"##### Screen Recording:\n-\n"
                   f"##### Sherlogs:\n-\n"
                   f"Attached Bugreport and Screen recording.")
        return _output


if __name__ == "__main__":
    # print(TableFormatter().bugTableFormatter())
    # print(TableFormatter().commentTableFormatter())
    print(Descriptor().comment_descriptor())
    print(Descriptor().bug_descriptor())
