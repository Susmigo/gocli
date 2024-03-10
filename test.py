# import requests
# from bs4 import BeautifulSoup
#
# data = ['com.google.android.apps.tv.launcherx']
#
# app_info_dict = {}
#
# for package_name in sorted(data):
#     url = f"https://play.google.com/store/apps/details?id={package_name}"
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'html.parser')
#
# app_info = {'url': r.url, 'package': package_name, 'title': soup.find('h1', {'itemprop': 'name'}).text.strip() if
# soup.find('h1', { 'itemprop': 'name'}) else "System App"}
#
#     # Extract version information
#     version_tag = soup.find('div', {'class': 'BgcNfc'})
#     app_info['version'] = version_tag.text.strip() if version_tag else "Version information not found"
#
#     app_info_dict[package_name] = app_info
#
#
import json
import platform
import subprocess

# import urllib.parse
#
# import bugdescriptor
#
browserPath = {
    'Darwin': "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "Linux": "/opt/google/chrome/google-chrome"}

#
# query = bugdescriptor.Descriptor.bugDescriptor()
# desc = urllib.parse.quote(query)
#
#
# def openChrome(link: str):
#     _platform = platform.system()
#     chromePath = browserPath.get(platform.system(), browserPath.get('Linux'))
#     args = ["--args", "--browser-startup-dialog", link]
#
#     command = [chromePath] + args
#     subprocess.Popen(command)
#
#
# openChrome(f"http://b/new?")


import os
import sys
import json


def find_chrome_user_data_dir():
    home = os.path.expanduser("~")
    platform_mapping = {
        'win32': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
        'darwin': os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome'),
        'linux': os.path.join(home, '.config', 'google-chrome')
    }
    return platform_mapping.get(sys.platform, None)


def find_local_state_file(chrome_user_data_dir):
    local_state_path = os.path.join(chrome_user_data_dir, "Local State")
    return local_state_path if os.path.exists(chrome_user_data_dir) and os.path.isfile(local_state_path) else None


def get_profiles_for_domain(local_state_path, domain):
    try:
        with open(local_state_path, 'r', encoding='utf-8') as file:
            local_state_data = json.load(file)

        profiles_info_cache = local_state_data.get('profile', {}).get('info_cache', {})
        profiles_for_domain = [profile for profile, profile_data in profiles_info_cache.items()
                               if 'hosted_domain' in profile_data and domain in profile_data['hosted_domain']]

        return profiles_for_domain

    except (FileNotFoundError, json.JSONDecodeError) as e:
        return f"Error reading Local State file: {e}"


def get_profiles_for_target_domain(domain:str):
    chrome_user_data_dir = find_chrome_user_data_dir()

    if not chrome_user_data_dir:
        return "Chrome user data directory not found."

    local_state_file = find_local_state_file(chrome_user_data_dir)

    if not local_state_file:
        return "Local State file not found in the Chrome user data directory."

    profiles_for_domain = get_profiles_for_domain(local_state_file, domain)

    if profiles_for_domain:
        return profiles_for_domain
    else:
        return f"No profiles found for domain '{domain}'."


def create_profile_file(res: str):
    home = os.path.expanduser("~")
    folder_path = os.path.join(home, '.config', 'gocli')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, 'profile.txt')

    if os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(res)
    else:
        return None


if __name__ == "__main__":
    create_profile_file(get_profiles_for_target_domain('google.com')[0])

# def verify_and_export_corp_profile(val: str):
#     corp_profile_value = os.getenv("CORP_PROFILE", val)
#
#     # Check if CORP_PROFILE is already set
#     if "CORP_PROFILE" in os.environ:
#         print("CORP_PROFILE is already set:", os.environ["CORP_PROFILE"])
#     else:
#         # Export to .bash_profile, .bashrc, and .zprofile
#         files_to_update = ["~/.zshrc"]
#
#         for file_path in map(os.path.expanduser, files_to_update):
#             with open(file_path, "a") as config_file:
#                 config_file.write(f'\nexport CORP_PROFILE="{corp_profile_value}"')
#
#         print(f"CORP_PROFILE set and exported to {', '.join(files_to_update)}\n Restart the terminal")
