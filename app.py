from bs4 import BeautifulSoup as bs
import requests
import re
import time
import notify2

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

notify2.init("cric-score")
url = "http://www.cricbuzz.com/cricket-match/live-scores"
r = requests.get(url)
data = r.text
soup = bs(data, "html.parser")
link = soup.find_all('a', class_='cb-lv-scrs-well-live')
match_url = "http://www.cricbuzz.com" + link[0].get('href')
print("Match URL: " + match_url)

while True:
    r = requests.get(match_url)
    data = r.text
    soup = bs(data, "html.parser")
    #print(soup.prettify())
    score = soup.find("span", class_="cb-font-20 text-bold", text=True)
    visible_texts = filter(visible, score)
    print(visible_texts[0])
    n = notify2.Notification("Live cricket score: ", visible_texts[0])
    n.show()
    time.sleep(10)
