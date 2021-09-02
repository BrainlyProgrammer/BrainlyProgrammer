import sys
import subprocess


def pip_install(module: str):
    subprocess.run([sys.executable, "-m", "pip", "-q", "--disable-pip-version-check", "install", module])


try:
    from bs4 import BeautifulSoup
except:
    print("'bs4' module not found! Trying to install... [GetTime_Lexi]")
    pip_install("bs4")
    from bs4 import BeautifulSoup

try:
    import requests
except:
    print("'requests' module not found! Trying to install... [GetTime_Lexi]")
    pip_install("requests")
    import requests

try:
    import re
except:
    print("'re' module not found! Trying to install... [GetTime_Lexi]")
    pip_install("re")
    import re


class GetTime:
    def __init__(self):
        self.place = None
        self.time = None
        self.date = None
        self.location = None

    def current_time(self, place):
        place = str(place)
        try:
            url = "https://www.google.com/search?q=time+now+in+" + place.replace(" ", "+")

            r = requests.get(url)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent, "html.parser")

            time = str(html_content.find("div", class_="BNeawe iBp4i AP7Wnd"))
            time = re.sub(r"(<.*?>)*", "", time)

            other_details = html_content.findAll("span", class_="r0bn4c rQMQod")

            date = str(other_details[1])
            date = str(re.sub(r"(<.*?>)*", "", date).split("\n")[0])

            location = str(other_details[0])
            location = re.sub(r"(<.*?>)*", "", location)

            if time is None or other_details is None:
                raise Exception("Something went wrong. No time found of the given place. ")

            self.place = place
            self.time = time
            self.date = date
            self.location = location

        except:
            raise Exception("Something went wrong. No time found of the given place. ")
