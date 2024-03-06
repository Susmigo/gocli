"""
Utilities that are re usuable in other scripts.
"""
import subprocess
import sys
from typing import Any

from rich.console import Console

console = Console()


def displayError(error_msg: str) -> None:
    """
    Displays the user given error msg
    :param error_msg: error msg given by user
    """
    console.print("\nERROR :exclamation: : " + error_msg, style="italic bold red", emoji=True)


def displaySuccess(info_msg: str) -> None:
    console.print("SUCCESS :rocket: : " + info_msg, style="bold green", emoji=True, new_line_start=True)


def displayInterrupt(info_msg: str) -> None:
    console.print("\nINTERRUPT :grey_exclamation: : " + info_msg, style="bold yellow", emoji=True)


def displayErrorExit(error_msg: str) -> Any:
    """
    Displays the user given error msg and exit
    :param error_msg: error msg given by user
    """
    console.print("\nERROR :bangbang: : " + error_msg, style="italic bold red", emoji=True)
    sys.exit(1)


def checkAdbDevices() -> bool:
    """
    Check for ADB installation and whether any device is connected to the laptop.
    :return: bool
    """
    # Check if ADB is installed
    try:
        subprocess.run(["adb", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        displayErrorExit("ADB is not installed or not in the system PATH.")

    # Check for connected devices
    devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)
    # Extract the list of devices
    device_lines = devices_result.stdout.strip().split('\n')[1:]

    if not any('device' in line for line in device_lines):
        displayErrorExit("No Device is connected. Connect a device 📲")
    else:
        return True


def runCommand(cmd: str) -> str:
    """
    Runs the adb commands using subprocess
    :param cmd:  adb command in string format
    :return: Output of the command as string
    """
    try:
        if checkAdbDevices():
            output = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            return output.stdout.strip()
    except subprocess.CalledProcessError as e:
        displayError(f"Error executing the command \n{e}.")
    except KeyboardInterrupt:
        displayErrorExit("Interrupted by User.")


if __name__ == "__main__":
    displayInterrupt('hi')
    displayError('lol')
    displaySuccess('success')
    print(checkAdbDevices())
    print(runCommand('adb hi'))
    displayErrorExit('hi')
