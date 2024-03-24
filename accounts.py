"""
This script lists and selects the accounts added in the connected device.
"""

from typing import Union

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from devicedetails import DeviceDetails
from utils.checks import Checks
from utils.commands import Commands
from utils.display import Display


class Accounts:
    def __init__(self):
        self.cmd = Commands()
        self.chk = Checks()
        self.display = Display()
        self.console = Console()
        self.device = DeviceDetails()

    def __list_accounts(self) -> list:
        """
        Displays the list of accounts in the device.
        :return: list
        """
        try:
            adb_command = "adb shell dumpsys account"
            output = self.cmd.adbCommand(adb_command)
            accounts = [line.split('=', 2)[1].split(',')[0] for line in output.strip().split('\n') if
                        line.startswith("    Account {name=")]
            return accounts
        except Exception as e:
            self.display.error_Exit('Something went wrong in Fetching the accounts.', trace=str(e))

    def __select_from_List(self) -> Union[str, None]:
        """
        Displays the list of accounts in the device and Prints the accounts based on User selection
        :return: Union[str, None]
        """
        accounts = self.__list_accounts()
        custom_option = len(accounts) + 1

        if accounts:
            options = accounts + ["Custom account"]

            # customizing the table
            table = Table(title=f"List of accounts in {self.device.getDeviceName()} device", highlight=True,
                          style="magenta", title_style="bold blue italic", )
            table.add_column("Id", justify="center", vertical="middle", )
            table.add_column("Accounts", justify="center", vertical="middle")

            # Display account options in the table.
            for idx, account in enumerate(options, start=1):
                table.add_row(str(idx), account, style="cyan", )
            self.console.print(table, new_line_start=True)  # printing the table

            # Get user input for selection.
            selection = Prompt.ask('Enter the account id in which issue is reproducing\n(Press ENTER for No account)')

            self.console.clear()

            # Check if the input is not empty before processing
            if selection and selection.isdigit() and 1 <= int(selection) <= custom_option:
                selected_index = int(selection) - 1
                if selected_index < len(accounts):
                    selected_account = options[selected_index]
                    return selected_account
                else:
                    custom_account = Prompt.ask("Enter the custom account")
                    self.console.clear()
                    return custom_account if str(custom_account).endswith('.com') else custom_account + '@gmail.com'
            else:
                self.console.print("Generating description with No account.")
                return None  # if user didn't enter any ID it returns None
        else:
            self.console.print("Generating description with No account.")

    def final_print(self) -> str:
        """
        Gives the list of accounts in string format.
        :return: str
        """
        _account = self.__select_from_List()
        return f"Account ID: {_account}" if _account is not None else ""

    def final_print_tabulate(self) -> list:
        """
        Gives the list of accounts in tabulate format.
        :return: list
        """
        _account = self.__select_from_List()
        return [["**Account ID**", _account]] if _account is not None else ""


if __name__ == "__main__":
    # print("For string:\n", Accounts().finalPrint())
    print("For tabulate:\n", Accounts().final_print_tabulate())
