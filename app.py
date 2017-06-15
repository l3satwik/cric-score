from bs4 import BeautifulSoup as bs
from random import *
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
