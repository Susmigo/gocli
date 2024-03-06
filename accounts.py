"""
This script lists and selects the accounts added in the connected device.
"""

from typing import Union

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from devicedetails import DeviceDetails
from utilities import runCommand, displayErrorExit

console = Console()


class Accounts:
    @classmethod
    def listAccounts(cls) -> list:
        try:
            adb_command = "adb shell dumpsys account"
            output = runCommand(adb_command)
            accounts = [line.split('=', 2)[1].split(',')[0] for line in output.strip().split('\n') if
                        line.startswith("    Account {name=")]
            return accounts
        except Exception:
            displayErrorExit('Something went wrong in Fetching the accounts.')

    @classmethod
    def selectFromList(cls) -> Union[str, None]:
        accounts = cls.listAccounts()
        custom_option = len(accounts) + 1
        options = accounts + ["Custom account"]

        # customizing the table
        table = Table(title=f"List of accounts in {DeviceDetails.getDeviceName()} device", highlight=True,
                      style="magenta", title_style="bold blue italic", )
        table.add_column("Id", justify="center", vertical="middle", )
        table.add_column("Accounts", justify="center", vertical="middle")

        # Display account options in the table
        for idx, account in enumerate(options, start=1):
            table.add_row(str(idx), account, style="cyan", )
        console.print(table, new_line_start=True)  # printing the table

        # Get user input for selection
        selection = Prompt.ask('Enter the account id in which issue is reproducing')

        console.clear()

        # Check if the input is not empty before processing
        if selection and selection.isdigit() and 1 <= int(selection) <= custom_option:
            selected_index = int(selection) - 1
            if selected_index < len(accounts):
                selected_account = options[selected_index]
                return selected_account
            else:
                custom_account = input("Enter the custom account: ")
                console.clear()
                return custom_account + '@gmail.com'
        else:
            return None  # if user didn't enter any ID it returns None

    @classmethod
    def finalPrint(cls) -> str:
        _account = cls.selectFromList()
        return f"Account ID: {_account}" if _account is not None else ""

    @classmethod
    def finalPrintTabulate(cls) -> list:
        """
        Prints the list of accounts in tabulate format
        :return: List of accounts in tabulate format
        """
        _account = cls.selectFromList()
        return [["**Account ID**", _account]] if _account is not None else ""


if __name__ == "__main__":
    # print("For string:\n", Accounts.finalPrint())
    print("For tabulate:\n", Accounts.finalPrintTabulate())
