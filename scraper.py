from urllib.request import urlopen
import bs4
from bs4 import re
import signal
import pickle

base_url = "https://www.youtube.com"

def make_dict(stem_url):
    soup = make_soup(base_url + stem_url)
    out_dict = {
        "name" : my_catch(base_url + stem_url, get_name, soup),
        "channel" : my_catch(base_url + stem_url, get_channel, soup),
        "views" : my_catch(base_url + stem_url, get_views, soup),
        "lnds" : my_catch(base_url + stem_url, get_LnDs, soup),
        "recommended" : my_catch(base_url + stem_url, get_recommended, soup),
    }
    return out_dict

def make_soup(url):
    return bs4.BeautifulSoup(urlopen(url), "lxml")

def get_name(soup):
    return soup.find("span", {"id" : "eow-title"}).attrs["title"]

def get_channel(soup):
    return soup.find("div", {"class" : "yt-user-info"}).find("a").text

def get_recommended(soup):
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
    cleaned_texts = [i.text.replace(",","") for i in button_content]
    lnds = even_indecies([i for i in cleaned_texts if i.isnumeric()])
    if len(lnds) != 2:
        # print("Error found on", get_name(soup))
        # [print(i.text) for i in button_content]
        # print("======== to ========")
        # [print(i) for i in cleaned_texts]
        # print([i for i in cleaned_texts if i.isnumeric()])
        # print("======== to ========")
        # print(lnds)
        raise IndexError("size mismatch")
        # return None
    ints = [int(i) for i in lnds]
    return (ints[0], ints[1], safe_ratio(ints))


def safe_ratio(ints):
    if sum(ints) == 0:
        return None
    else:
        return ints[0] / sum(ints)

def even_indecies(lst):
    return [lst[i] for i in range(len(lst)) if i % 2 == 0]

def even_indecies_aux(lst):
    """faster but a touch less readable"""
    return [lst[i] for i in range((len(lst) + 1) // 2)]

def cb_sigint_handler(signum, stack):
    global run
    print("SIGINT received")
    run = False

def my_catch(url, f, soup):
    try:
        return f(soup)
    except Exception as e:
        print(url, repr(f), e)
        return None

if __name__ == '__main__':
    data_store = []
    active = ["/watch?v=VGCE_3fjzU4"]
    explored = []
    # soup = make_soup(base_url + "/watch?v=VGCE_3fjzU4")
    # print(make_dict(stem))
    run = True
    signal.signal(signal.SIGINT, cb_sigint_handler)
    while run and len(active) > 0:
        try:
            temp_url = active.pop()
            temp_dict = make_dict(temp_url)
            explored.append(temp_url)
            for rec in temp_dict["recommended"]:
                if not (rec in explored or rec in active):
                    active.append(rec)
            data_store.append(temp_dict)
        except Exception as e:
            print("this happened", e)
            run = False

    print("length of data_store:", len(data_store))

    with open("data_store", "wb") as f:
        pickle.dump(data_store, f)
    with open("active", "wb") as g:
        pickle.dump(active, g)
    with open("explored", "wb") as h:
        pickle.dump(explored, h)
