from urllib import request

if __name__ == "__main__":
    response = request.urlopen("http://www.example.com/")
    html = response.read()
    html = html.decode("utf-8")
    print(html)
