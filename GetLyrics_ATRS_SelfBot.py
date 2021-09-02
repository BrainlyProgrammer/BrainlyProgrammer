import sys
import subprocess
import urllib3
import certifi


def pip_install(module: str):
    subprocess.run([sys.executable, "-m", "pip", "-q", "--disable-pip-version-check", "install", module])


try:
    from bs4 import BeautifulSoup
except:
    print("'bs4' module not found! Trying to install... [GetLyrics_Lexi]")
    pip_install("bs4")
    from bs4 import BeautifulSoup

try:
    import requests
except:
    print("'requests' module not found! Trying to install... [GetLyrics_Lexi]")
    pip_install("requests")
    import requests

try:
    import re
except:
    print("'re' module not found! Trying to install... [GetLyrics_Lexi]")
    pip_install("re")
    import re

try:
    import urllib.request
except:
    print("'urllib' module not found! Trying to install... [GetLyrics_Lexi]")
    pip_install("urllib")
    import urllib.request

try:
    import json
except:
    print("'json' module not found! Trying to install... [GetLyrics_Lexi]")
    pip_install("json")
    import json


class GetLyrics:
    def __init__(self):
        self.title = None
        self.artist = None
        self.lyrics = None
        self.source = None
        self.query = None
        self.api_key = None
        self.url = None

    def google_lyrics(self, query):
        query = str(query)
        try:
            url = "https://www.google.com/search?q=" + query.replace(" ", "+") + "+lyrics"

            r = requests.get(url)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent, "html.parser")

            title = str(html_content.find("span", class_="BNeawe tAd8D AP7Wnd"))
            title = re.sub(r"(<.*?>)*", "", title).replace("[", "").replace("]", "")

            artist = html_content.find_all("span", class_="BNeawe s3v9rd AP7Wnd")
            artist = str(artist[1])
            artist = re.sub(r"(<.*?>)*", "", artist).replace("[", "").replace("]", "")

            lyrics = html_content.find_all("div", class_="BNeawe tAd8D AP7Wnd")
            lyrics = str(lyrics[2])
            lyrics = re.sub(r"(<.*?>)*", "", lyrics).replace("[", "").replace("]", "")

            source = str(html_content.find("span", class_="uEec3 AP7Wnd"))
            source = re.sub(r"(<.*?>)*", "", source).replace("[", "").replace("]", "")

            if lyrics is None or artist is None or title is None or source is None:
                raise Exception("Something went wrong. No lyrics yielded. ")

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = source  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = None  # API Key provided by the user (Here not required)
            self.url = None
        except:
            raise TimeoutError

    def genius_lyrics(self, query, api_key):
        query = str(query)
        api_key = str(api_key)
        try:
            url = "https://api.genius.com/search?access_token=" + api_key + "&q=" + query.replace("&",
                                                                                                  "and").replace(
                "by", "-").replace(" ", "%20")
            details = urllib.request.urlopen(url).read().decode()
            json_results = json.loads(details)

            title = str(json_results["response"]["hits"][0]["result"]["title"])
            artist = str(json_results["response"]["hits"][0]["result"]["primary_artist"]["name"])
            genius_url = str(json_results["response"]["hits"][0]["result"]["url"])
            url1 = genius_url
            r = requests.get(url1)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent.decode("utf-8").replace("<br/>", "\n"), "html.parser")

            lyrics = str(html_content.find("div", class_=re.compile("^lyrics$|Lyrics__Root")).get_text())
            lyrics = re.sub(r"(\[.*?])*", "", lyrics).replace("\n\n", "\n")

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = "Genius"  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = api_key  # API Key provided by the user
            self.url = url1
        except:
            raise TimeoutError

    def musixmatch_lyrics(self, query):
        query = str(query)
        try:
            url = 'https://www.musixmatch.com/search/' + query.replace(" ", "%20")  # +'/lyrics'
            http = urllib3.PoolManager(ca_certs=certifi.where())
            resp = http.request('GET', url)
            r = resp.data.decode('utf-8')
            html_content = BeautifulSoup(r, "html.parser")
            href = str(html_content.find("a", class_="title")).split("href=")[1].split('''"''')[1]
            new_link = "https://www.musixmatch.com/" + href
            http = urllib3.PoolManager(ca_certs=certifi.where())
            url = new_link
            resp = http.request('GET', url)
            r = resp.data.decode('utf-8')
            html_content = BeautifulSoup(r, "html.parser")

            artist = str(html_content.find("a", class_="mxm-track-title__artist mxm-track-title__artist-link"))
            artist = re.sub(r"(<.*?>)*", "", artist)

            title = str(html_content.find("h1", class_="mxm-track-title__track").getText("//")).split("//")[-1]
            title = re.sub(r"(<.*?>)*", "", title)

            lyrics = html_content.findAll("span", class_="lyrics__content__ok")
            lyrics = str(lyrics[0]) + "\n" + str(lyrics[1])
            lyrics = re.sub(r"(<.*?>)*", "", lyrics)

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = "Musixmatch"  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = None  # API Key provided by the user
            self.url = new_link
        except:
            raise TimeoutError
