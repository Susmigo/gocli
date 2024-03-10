"""
Utilities that are re usuable in other scripts.
"""
import json
import os
import subprocess
import sys
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
        self.console.print("\n INFO :information_desk_person: :" + info_msg, style="italic", emoji=True)

    def displaySuccess(self, info_msg: str) -> None:
        self.console.print("SUCCESS :rocket: : " + info_msg, style="bold green", emoji=True, new_line_start=True)

    def displayInterrupt(self, info_msg: str) -> None:
        self.console.print("\nINTERRUPT :grey_exclamation: : " + info_msg, style="bold yellow", emoji=True)

    def displayErrorExit(self, error_msg: str) -> Any:
        """
        Displays the user given error msg and exit
        :param error_msg: error msg given by user
        """
        self.console.print("\nERROR :bangbang: : " + error_msg, style="italic bold red", emoji=True)
        sys.exit()


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
            self.displayError(f"Error executing the command \n{e}.")
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


if __name__ == "__main__":
    # err = Errors()
    # chk = Checks()
    # cmd = Commands()
    #
    # err.displayInterrupt('hi')
    # err.displayError('lol')
    # err.displaySuccess('success')
    # print(chk.checkAdbDevices())
    # print(cmd.runCommand('adb hi'))
    # err.displayErrorExit('hi')
    cp = ChromeProfile()
    # print(cp.getChromeUserDir())
    # print(cp.fetchProfile('google.com'))
    # print(cp.saveToConfig())
    print(cp.getProfileFromConfig())
    print(cp.saveToConfig())
