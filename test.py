"""
This class simply acts as a sandbox to test individual functions before implementation in the main bot
"""
import urllib.parse
import urllib.request
import bs4

def search(search_query):
    query = urllib.parse.quote(search_query)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    find = soup.findAll(attrs={'class':'yt-uix-tile-link'})
    print("https://www.youtube.com" + find[0]['href'])

search("thrift shop")