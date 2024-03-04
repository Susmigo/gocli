"""
Utilities that are re usuable in other scripts
"""
import subprocess
import sys

import typer


def display_error(info_msg: str):
    """
    Displays the user given error msg
    :param info_msg: error msg given by user
    """
    message = typer.style("Error:", fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True)
    typer.echo(message + " " + info_msg)


def display_error_exit(info_msg: str):
    """
    Displays the user given error msg and exit
    :param info_msg: error msg given by user
    """
    message = typer.style("Error:", fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True)
    typer.echo(message + " " + info_msg)
    sys.exit(1)


def check_adb_devices() -> bool:
    """
    Check for ADB installation and whether any device is connected to the laptop.
    :return:
    """
    # Check if ADB is installed
    try:
        subprocess.run(["adb", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        display_error_exit("ADB is not installed or not in the system PATH.")

    # Check for connected devices
    devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)
    # Extract the list of devices
    device_lines = devices_result.stdout.strip().split('\n')[1:]

    if not any('device' in line for line in device_lines):
        display_error_exit("No Device is connected. Connect a device 📲")
    else:
        return True


def _run_command(cmd: str) -> str:
    """
    Runs the adb commands using subprocess
    :param cmd:  adb command in string format
    :return: Output of the command as string
    """
    try:
        if check_adb_devices():
            output = subprocess.run(cmd, shell=True, check=True, capture_output=True,
                                    text=True)
            return output.stdout.strip()
    except subprocess.CalledProcessError as e:
        display_error(f"Error executing the command \n{e}.")
    except KeyboardInterrupt:
        display_error("Interrupted by User.")
