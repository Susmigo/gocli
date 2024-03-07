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
#     app_info = {'url': r.url, 'package': package_name,
#                 'title': soup.find('h1', {'itemprop': 'name'}).text.strip() if soup.find('h1',
#                                                                                          {
#                                                                                              'itemprop': 'name'}) else "System App"}
#
#     # Extract version information
#     version_tag = soup.find('div', {'class': 'BgcNfc'})
#     app_info['version'] = version_tag.text.strip() if version_tag else "Version information not found"
#
#     app_info_dict[package_name] = app_info
#
#
# import platform
# import subprocess
# import urllib.parse
#
# import bugdescriptor
#
# browserPath = {
#     'Darwin': "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
#     "Linux": "/opt/google/chrome/google-chrome"}
#
# query = bugdescriptor.Descriptor.bugDescriptor()
# desc = urllib.parse.quote(query)
#
#
# def openChrome(link: str):
#     _platform = platform.system()
#     chromePath = browserPath.get(platform.system(), browserPath.get('Linux'))
#     args = ["--args", "--profile-directory=Default", link]
#
#     command = [chromePath] + args
#     subprocess.Popen(command)
#
#
# openChrome(f"http://b/new?&description={desc}&format=MARKDOWN")
