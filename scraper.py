from urllib.request import urlopen
import bs4
from bs4 import re

base_url = "https://www.youtube.com"

def get_recommended(soup):
    return [i.attrs["href"] for i in soup.find_all("a",{"class" : "content-link"})]

def get_views(soup):
    raw_string = soup.find("div", {"class" : "watch-view-count"}).text
    return int(re.sub(r"[^0-9]", "", raw_string))

def get_LnDs(soup):
    button_content = soup.find_all("span", {"class" : "yt-uix-button-content"})
    lnds = even_indecies([i.text for i in button_content if i.text.isnumeric()])
    return tuple(int(i) for i in lnds)

def even_indecies(lst):
    return [lst[i] for i in range(len(lst)) if i % 2 == 0]

def even_indecies_aux(lst):
    """faster but a touch less readable"""
    return [lst[i] for i in range((len(lst) + 1) // 2)]

if __name__ == '__main__':
    pass
    # main()
