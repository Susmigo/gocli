"""
Utilities that are re usuable in other scripts.
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
import requests
from typing import Any

from rich.console import Console


class Errors:
    """
    Shows custom errors, info and success messages in the terminal.
    """

    def __init__(self):
        self.console = Console()

    def displayError(self, error_msg: str) -> None:
        """
        Displays the user given error msg
        :param error_msg: error msg given by user
        """
        self.console.print("\nERROR :exclamation: : " + error_msg, style="italic bold red", emoji=True)

    def displayInfo(self, info_msg: str) -> None:
        self.console.print("\nINFO :information_desk_person: : " + info_msg, style="italic", emoji=True)

    def displaySuccess(self, info_msg: str) -> None:
        self.console.print("SUCCESS :rocket: : " + info_msg, style="bold green", emoji=True, new_line_start=True)

    def displayInterrupt(self, info_msg: str) -> None:
        self.console.print("\nINTERRUPT :grey_exclamation: : " + info_msg, style="bold yellow", emoji=True)
        sys.exit(1)

    def displayErrorExit(self, error_msg: str) -> Any:
        """
        Displays the user given error msg and exit
        :param error_msg: error msg given by user
        """
        self.console.print("\nERROR :bangbang: : " + error_msg, style="italic bold red", emoji=True)
        sys.exit(1)


class Checks(Errors):
    """
    Adb checks before executing any command.
    """

    def __init__(self):
        super().__init__()

    def checkAdbDevices(self) -> bool:
        """
        Check for ADB installation and whether any device is connected to the laptop.
        :return: bool
        """
        # Check if ADB is installed
        try:
            subprocess.run(["adb", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError:
            self.displayErrorExit("ADB is not installed or not in the system PATH.")

        # Check for connected devices
        devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True)
        # Extract the list of devices
        device_lines = devices_result.stdout.strip().split('\n')[1:]

        if not any('device' in line for line in device_lines):
            self.displayErrorExit("No Device is connected. Connect a device 📲")
        else:
            return True


class Commands(Checks):
    """
    Subprocess commands for running adb commands.
    """

    def __init__(self):
        super().__init__()

    def runCommand(self, _cmd: str) -> str:
        """
        Runs the adb commands using subprocess
        :param _cmd:  adb command in string format
        :return: Output of the command as string
        """
        try:
            if self.checkAdbDevices():
                output = subprocess.run(_cmd, shell=True, check=True, capture_output=True, text=True)
                return output.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.displayErrorExit(f"Error executing the command \n >> {e}.")
        except KeyboardInterrupt:
            self.displayErrorExit("Interrupted by User.")

    def runSubprocess(self, _cmd: str) -> str | tuple[int, str]:
        try:
            # Execute the command and capture stdout and stderr
            result = subprocess.run(_cmd, shell=True, capture_output=True, text=True)
            # Check if the command was successful
            if result.returncode == 0:
                return result.stdout.strip()  # No error, return stdout
            else:
                return result.returncode, result.stderr.strip()  # Return stderr if there's an error
        except Exception as e:
            return str(e)  # Return the exception message as stderr
        except KeyboardInterrupt:
            self.displayErrorExit("Interrupted by User.")


class ChromeProfile(Errors):
    """
    Fetches the chrome profile based on the hosted domain.
    """

    def __init__(self):
        super().__init__()
        self.home = os.path.expanduser('~')
        self.__file_path = __file_path = os.path.join(self.home, '.config', 'gocli', 'config')

    @staticmethod
    def getChromeUserDir() -> str:
        home = os.path.expanduser("~")
        platforms = {
            'win32': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
            'darwin': os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome'),
            'linux': os.path.join(home, '.config', 'google-chrome')
        }

        return platforms.get(sys.platform, None)

    def fetchProfile(self, domain: str):
        user_dir = self.getChromeUserDir()

        # profiles are stored in the Local State file in chrome user data directory.
        local_file_path = os.path.join(user_dir, 'Local State')

        if os.path.exists(user_dir) and os.path.isfile(local_file_path):
            try:
                with open(local_file_path, 'r', encoding='utf-8') as file:
                    local_state_data = json.load(file)

                # Getting the files from the json file of Local State.
                profiles_data = local_state_data.get('profile', {}).get('info_cache', {})

                # Getting profile names based on hosted domain.
                profiles = [profile for profile, profile_data in profiles_data.items()
                            if 'hosted_domain' in profile_data and domain in profile_data['hosted_domain']]
                if profiles:
                    return profiles[0]
                else:
                    self.displayError(f"No profiles found for domain '{domain}'.")
            except (FileNotFoundError, json.JSONDecoder):
                self.displayErrorExit("failed to get the Chrome profile.")

    def saveToConfig(self) -> str:
        profile = self.fetchProfile('google.com')
        config_dir = os.path.join(self.home, '.config', 'gocli')
        os.makedirs(config_dir, exist_ok=True)
        config_file = self.__file_path
        with open(config_file, 'w') as file:
            file.write(profile)
        return profile

    def getProfileFromConfig(self) -> str:
        file_path = self.__file_path
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            self.displayInfo('No file exists .. creating one.')
            return self.saveToConfig()


class HandleFiles(Errors):

    def __init__(self):
        super().__init__()
        self.home = os.path.expanduser('~')

    def checkDir(self, folder: str) -> bool:
        dir_path = os.path.join(self.home, folder)
        return os.path.exists(dir_path) and os.path.isdir(dir_path)

    def makeDir(self, folder: str) -> str:
        path = os.path.join(self.home, folder)
        os.makedirs(path, exist_ok=True)
        return path

    def moveOrCopyFiles(self, _ext: list, path: str, is_copy: bool = False, _start_name: str = ""):
        destination_path = os.path.join(self.home, path)
        if not self.checkDir(destination_path):
            self.makeDir(destination_path)
        try:
            for _ in os.listdir(self.home):
                if any(_.endswith(ext) and _.startswith(_start_name) for ext in _ext):
                    file = os.path.join(self.home, _)
                    self.console.print("Found existing files\n")
                    if is_copy:
                        shutil.copy(file, destination_path)
                        self.console.print(f'{_} copied to {destination_path}\n')
                    else:
                        try:
                            self.console.print(f'{_} moved to {destination_path}\n')
                            shutil.move(file, destination_path)
                        except shutil.Error:
                            self.console.print('File already exists...')
        except FileNotFoundError:
            self.console.print('File not found...')


class NetworksOps(Errors):
    def __init__(self):
        super().__init__()

    def checkNetwork(self) -> bool:
        try:
            response = requests.get("http://www.google.com", timeout=5)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.ConnectionError:
            self.displayErrorExit("No Network. Connect to any and try again.")


if __name__ == "__main__":
    # err = Errors()
    # chk = Checks()
    # cmd = Commands()
    # stdout = cmd.runSubprocess('command -V snipit')
    # print(stdout)
    # err.displayInterrupt('hi')
    # err.displayError('lol')
    # err.displaySuccess('success')
    # print(chk.checkAdbDevices())
    # print(cmd.runCommand('adb hi'))
    # err.displayErrorExit('hi')
    # cp = ChromeProfile()
    # print(cp.getChromeUserDir())
    # print(cp.fetchProfile('google.com'))
    # print(cp.saveToConfig())
    # print(cp.getProfileFromConfig())
    # print(cp.saveToConfig())
    # hf = HandleFiles()
    # print(hf.moveOrCopyFiles(['.zip'], 'bug reports', is_copy=False))

    # networkops
    np = NetworksOps()
    if True & np.checkNetwork():
        print('pass')
