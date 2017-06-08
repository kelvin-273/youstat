# youstats
This web scraper crawls around Youtube collecting analytics from each video.
The information collected includes view-count, likes, dislikes, title and
channel.

## Usage
`python scraper.py` begins running the scraper. `Ctrl + c` to terminate while
running. This saves whatever progress has been made to pickle dumps:
- **data_store** is a list of dictionaries with all the scraped information.
- **active** is the list of addresses queued for scraping.
- **explored** is the list of addresses that have already been scraped.

## Todo
- [ ] Check for dropped request
- [ ] Resend dropped request
- [ ] Load previous saves
- [ ] Module for analysing the stats
- [ ] NLP module for the title
- [ ] Scrape comments
- [ ] Generalise scraping algorithm

## Requirements
- BeautifulSoup4
- Matplotlib
- Seaborn
- Pandas
