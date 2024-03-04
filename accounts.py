"""
This script lists and selects the accounts added in the connected device.
"""
from typing import Union

from utilities import _run_command, display_error_exit


class Accounts:
    @classmethod
    def _listAccounts(cls) -> list:
        try:
            adb_command = "adb shell dumpsys account"
            output = _run_command(adb_command)
            accounts = [line.split('=', 2)[1].split(',')[0]
                        for line in output.strip().split('\n')
                        if line.startswith("    Account {name=")]
            return accounts
        except Exception:
            display_error_exit('Something went wrong in Fetching the accounts.')

    @classmethod
    def select_from_list(cls) -> Union[str, None]:
        accounts = cls._listAccounts()
        custom_option = len(accounts) + 1
        options = accounts + ["Custom account"]

        # Display account options
        for idx, account in enumerate(options, start=1):
            print(f"{idx}. {account}")

        # Get user input for selection
        selection = input("Choose the account id in which it is reproducing: ")
        # Check if the input is not empty before processing
        if selection and selection.isdigit() and 1 <= int(selection) <= custom_option:
            selected_index = int(selection) - 1
            if selected_index < len(accounts):
                selected_account = options[selected_index]
                return selected_account
            else:
                custom_account = input("Enter the custom account: ")
                return custom_account + '@gmail.com'
        else:
            return None

    @classmethod
    def final_print_str(cls) -> str:
        account = cls.select_from_list()
        return f"Account ID: {account}" if account is not None else ""

    @classmethod
    def final_print_for_tabulate(cls) -> list:
        """
        Prints the list of accounts in tabulate format
        :return: List of accounts in tabulate format
        """
        account = cls.select_from_list()
        return [["**Account ID**", account]] if account is not None else ""


if __name__ == "__main__":
    print("For string:\n", Accounts.final_print_str())
    print("For tabulate:\n", Accounts.final_print_for_tabulate())
