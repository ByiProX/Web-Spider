# Opens several Baidu search results.

import requests, sys, webbrowser, bs4

print('Baiduing...') # display text while downloading the Baidu page
url = 'http://www.baidu.com/s?wd=' + ' '.join(sys.argv[1:])
res = requests.get(url)
res.raise_for_status()

# Retrieve top search result links.
soup = bs4.BeautifulSoup(res.text,'html.parser')

# # Open a browser tab for each result.
linkElems = soup.select('.t a')
# print(linkElems[1])
numOpen = min(5, len(linkElems))
for i in range(numOpen):
    webbrowser.open(linkElems[i].get('href'))
