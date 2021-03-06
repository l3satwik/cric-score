from bs4 import BeautifulSoup as bs
from random import *
import requests
import re
import time
import notify2
from pushbullet import Pushbullet

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

api_key = raw_input("Enter your API Key ('0' if you don't want Pushbullet notifications): ")
if api_key != "0":
    pb = Pushbullet(api_key)
notify2.init("cric-score")
url = "http://www.cricbuzz.com/cricket-match/live-scores"
try:
    r = requests.get(url)
except Exception:
    print("Please check your internet connection and try again!")
    raise SystemExit
data = r.text
soup = bs(data, "html.parser")
link = soup.find_all('a', class_='cb-lv-scrs-well-live')
try:
    match_url = "http://www.cricbuzz.com" + link[0].get('href')
except Exception:
    print("Cricbuzz is using another HTML structure!")
    raise SystemExit
print("Match URL: " + match_url)
no6 = 0
noW = 0
while True:
    r = requests.get(match_url)
    data = r.text
    soup = bs(data, "html.parser")
    #print(soup.prettify())
    score = soup.find("span", class_="cb-font-20 text-bold", text=True)
    visible_score = filter(visible, score)
    print(visible_score[0])
    n = notify2.Notification("Live cricket score: ", visible_score[0])
    n.show()
    update = soup.find("div", class_="cb-col cb-col-100 cb-font-12 cb-text-gray cb-min-rcnt")
    children = update.findChildren()
    visible_update = filter(visible, children[1])

    if visible_update[0].count('6') > no6:
        print("### 6 ###")
        n = notify2.Notification("### 6 ###")
        n.show()
        if api_key != "0":
            motog = pb.devices[1] #currently only for my phone
            push = pb.push_note("Cricket Notification", "6 has been hit!!", device=motog)
        no6 = visible_update[0].count('6')
    else:
        no6 = visible_update[0].count('6')

    #if visible_update[0].count('W') > noW:
    #    print("### W ###")
    #    n = notify2.Notification("### W ###")
    #    n.show()
    #    noW = visible_update[0].count('W')
    #else:
    #    noW = visible_update[0].count('W')

    time.sleep(randint(1,100))
