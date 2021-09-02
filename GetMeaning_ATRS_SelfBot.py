import sys
import subprocess


def pip_install(module: str):
    subprocess.run([sys.executable, "-m", "pip", "-q", "--disable-pip-version-check", "install", module])


try:
    from bs4 import BeautifulSoup
except:
    print("'bs4' module not found! Trying to install... [GetMeaning_Lexi]")
    pip_install("bs4")
    from bs4 import BeautifulSoup

try:
    import requests
except:
    print("'requests' module not found! Trying to install... [GetMeaning_Lexi]")
    pip_install("requests")
    import requests

try:
    import re
except:
    print("'re' module not found! Trying to install... [GetMeaning_Lexi]")
    pip_install("re")
    import re


class GetMeaning:
    def __init__(self):
        self.query = None
        self.word = None
        self.part_of_speech = None
        self.defination = None
        self.use = None

    def meaning(self, query):
        query = str(query)

        try:
            url = "https://www.google.com/search?q=define+" + query.replace(" ", "+")
            r = requests.get(url)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent, "html.parser")

            word = str(html_content.find("div", class_="BNeawe deIvCb AP7Wnd"))
            word = str(re.sub(r"(<.*?>)*", "", word)).strip().capitalize()

            part_of_speech = str(html_content.find_all("span", class_="r0bn4c rQMQod")[0])
            part_of_speech = str(re.sub(r"(<.*?>)*", "", part_of_speech)).strip().capitalize()

            meaning = str(html_content.find("div", class_="v9i61e"))
            meaning = str(re.sub(r"(<.*?>)*", "", meaning)).strip().capitalize()

            use = str(html_content.find_all("span", class_="r0bn4c rQMQod")[1])
            use = str(re.sub(r"(<.*?>)*", "", use)).replace("'", "").strip().capitalize()

            if word == "None" or part_of_speech == "None" or meaning == "None" or use == "None":
                raise Exception("Something went wrong. No meaning found. ")

            self.query = query
            self.word = word
            self.part_of_speech = part_of_speech
            self.defination = meaning
            self.use = use

        except:
            raise Exception("Something went wrong. No meaning found. ")
