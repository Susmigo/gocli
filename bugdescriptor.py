"""
This file gives the Bug description based on the user input.
"""

from tabulate import tabulate

from accounts import Accounts
from apkdetails import ApkDetails
from devicedetails import DeviceDetails


class TableFormatter:
    @staticmethod
    def tableFormatter():
        headers = ['Environment', ' Details']
        table = []
        table.extend(DeviceDetails().final_print_for_tabulate())
        table.extend(ApkDetails().final_print_for_tabulate())
        table.extend(Accounts().final_print_for_tabulate())
        return tabulate(table, headers, tablefmt="pipe")


if __name__ == "__main__":
    print(TableFormatter.tableFormatter())
