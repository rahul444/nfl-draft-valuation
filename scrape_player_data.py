import bs4 as bs
import urllib.request

URL = ""

source = urllib.request.urlopen(URL).read()
print(source)