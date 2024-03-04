import requests
from bs4 import BeautifulSoup


data = ['com.google.android.apps.tv.launcherx']

app_info_dict = {}

for package_name in sorted(data):
    url = f"https://play.google.com/store/apps/details?id={package_name}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    app_info = {'url': r.url, 'package': package_name,
                'title': soup.find('h1', {'itemprop': 'name'}).text.strip() if soup.find('h1',
                                                                                         {
                                                                                             'itemprop': 'name'}) else "System App"}

    # Extract version information
    version_tag = soup.find('div', {'class': 'BgcNfc'})
    app_info['version'] = version_tag.text.strip() if version_tag else "Version information not found"

    app_info_dict[package_name] = app_info

print(app_info_dict)