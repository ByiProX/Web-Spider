import requests

url = 'https://stackoverflow.com/users/7544402/byiprox'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'referer': 'https://stackoverflow.com',
    'cookie': 'prov=f90f4d3b-ab7c-c358-00d9-ad7b1f0fe234; _ga=GA1.2.2077515371.1536890624; __qca=P0-938784580-1536890626258; notice-ctt=4%3B1542002771699; _gid=GA1.2.1300082252.1552808838; acct=t=KPMZMpwQVjAp9oGeUkudAAsmzj3N5EXe&s=JtZxCk1kx9pGdYybKQVEt6DFSL3RbgGj'
}

res = requests.get(url=url, headers=headers)
print(res)