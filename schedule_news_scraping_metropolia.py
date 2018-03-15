import datetime
import timeit
import feedparser as fp
import requests as rq
from bs4 import BeautifulSoup
import calendar


# schedule scraping
infos = []
today = str(datetime.date.today())
print(today)
page = 'https://lukkarit.metropolia.fi/toteutuksenVarausLista.php?code=TX00CP84-3003'
page_get = rq.get(page)

page_analysis = BeautifulSoup(page_get.text, 'html5lib')
calendar_school = page_analysis.find_all('td')
for info in calendar_school:
    infos.append(info.get_text())

for i in range(0, len(infos) + 1):
    try:
        if today == infos[i][0:10]:
            print("Your schedule for today:")
            break
    except IndexError:
        print("You do not have class today.")

for i in range(0, len(infos)):
    if today == infos[i][0:10]:
        print("Time:", infos[i + 2])
        print("Location:", infos[i + 3])
        print("Course:", infos[i + 5])
        print("Teacher:", infos[i + 7])
        print("")

# news scraping
d = fp.parse(
    'http://www.metropolia.fi/en/about-us/news-and-events/?type=100&tx_ttnews%5Bcat%5D=44&cHash=2a190cbca72a7cc181781059d2c26b07')
if today != d.feed.updated[0:10]:
    print('There is no news today.\nHowever, there are 2 recent news:')
    for i in range(0, 2):
        print('Title:', d.entries[i].title)
        print('Link:', d.entries[i].link)
else:
    print('There is a news today.\nHere it is:')
    print('Title:', d.entries[0].title)
    print('Link:', d.entries[0].link)
print("")

# menu Unicafe scraping

today_1 = calendar.day_name[datetime.date.today().weekday()]
parse_link = fp.parse('https://messi.hyyravintolat.fi/rss/eng/9')
print("Here is a menu in UNICAFE today:")
for n in range(0, 7):
    if today_1 in parse_link.entries[n].title:
        print(parse_link.entries[n].title)
        menu = parse_link.entries[n].summary
        items = menu.split(sep='.')
        for item in items:
            print(item.strip())
        break
