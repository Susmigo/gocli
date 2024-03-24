import json
import os
import sys

from utils.display import Display


class ChromeProfile:
    """
    Fetches the chrome profile based on the hosted domain.
    """

    def __init__(self):
        self.home = os.path.expanduser('~')
        self.display = Display()
        self.__file_path = __file_path = os.path.join(self.home, '.config', 'gocli', 'config')

    @staticmethod
    def getChromeUserDir() -> str:
        home = os.path.expanduser("~")
        platforms = {'win32': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
                     'darwin': os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome'),
                     'linux': os.path.join(home, '.config', 'google-chrome')}

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
                profiles = [profile for profile, profile_data in profiles_data.items() if
                            'hosted_domain' in profile_data and domain in profile_data['hosted_domain']]
                if profiles:
                    return profiles[0]
                else:
                    self.display.error(f"No profiles found for domain '{domain}'.")
            except (FileNotFoundError, json.JSONDecoder):
                self.display.error_Exit("failed to get the Chrome profile.")

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
            self.display.info('No file exists .. creating one.')
            return self.saveToConfig()


if __name__ == "__main__":
    cp = ChromeProfile()
    print(cp.getChromeUserDir())
    print(cp.fetchProfile('google.com'))
    print(cp.saveToConfig())
    print(cp.getProfileFromConfig())
