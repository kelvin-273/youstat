from urllib.request import urlopen
import bs4
from bs4 import re

base_url = "https://www.youtube.com"

def make_dict(stem_url):
    soup = make_soup(base_url + stem_url)
    out_dict = {
        "name" : get_name(soup),
        "channel" : get_channel(soup),
        "views" : get_views(soup),
        "lnds" : get_LnDs(soup),
        "rec" : get_recommendeds(soup),
    }
    return out_dict

def make_soup(url):
    return bs4.BeautifulSoup(urlopen(url), "lxml")

def get_name(soup):
    return soup.find("span", {"id" : "eow-title"}).attrs["title"]

def get_channel(soup):
    return soup.find("div", {"class" : "yt-user-info"}).find("a").text

def get_recommendeds(soup):
    return [i.attrs["href"] for i in soup.find_all("a",{"class" : "content-link"})]

def get_views(soup):
    raw_string = soup.find("div", {"class" : "watch-view-count"}).text
    return int(re.sub(r"[^0-9]", "", raw_string))

def get_LnDs(soup):
    """
    extracts a tuple of the likes, dislikes and ratio of likes to total
    sentiments from the soup of a given video page
    """
    button_content = soup.find_all("span", {"class" : "yt-uix-button-content"})
    lnds = even_indecies([i.text for i in button_content if i.text.isnumeric()])
    assert len(lnds) == 2
    ints = [int(i) for i in lnds]
    return (ints[0], ints[1], ints[0] / sum(ints))

def even_indecies(lst):
    return [lst[i] for i in range(len(lst)) if i % 2 == 0]

def even_indecies_aux(lst):
    """faster but a touch less readable"""
    return [lst[i] for i in range((len(lst) + 1) // 2)]

if __name__ == '__main__':
    stem = "/watch?v=VGCE_3fjzU4"
    # soup = make_soup(base_url + "/watch?v=VGCE_3fjzU4")
    print(make_dict(stem))
