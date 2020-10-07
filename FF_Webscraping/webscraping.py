import pandas
import requests
from bs4 import BeautifulSoup
from datetime import datetime

r = requests.get("https://www.vegasinsider.com/nfl/odds/las-vegas/", headers={
                 'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content

soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("table", {"class": "frodds-data-tbl"})

weatherr = requests.get("https://rotogrinders.com/weather/nfl", headers={
                        'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
weatherc = weatherr.content
weathersoup = BeautifulSoup(weatherc, "html.parser")

weatherall = weathersoup.find_all("div", {"class": "crd"})

weatherd = {}
for tab in weatherall:
  teams = [x.text for x in tab.find_all("span", {"class": "lng"})]
  weathertable = [x.text for x in tab.find_all("span", {"class": "display"})]
  if weathertable == []:
    weathertable.append("Dome")
  else:
    weathertable = weathertable[1:3] + weathertable[4:]
  if len(weathertable) > 1:
    weatherd[teams[1]] = {
        "Temperature": weathertable[0],
        "Precipitation": weathertable[1],
        "Wind Direction": weathertable[2],
        "Wind Speed": weathertable[3]
    }
  else:
    weatherd[teams[1]] = {
        "Temperature": "Dome",
        "Precipitation": "Dome",
        "Wind Direction": "Dome",
        "Wind Speed": "Dome"
    }

table = all[0].find_all("tr")


l = []

for a in table:
  d = {}
  teams = a.find_all("b")
  odds = a.find_all("td", {"class": "oddsCell"})
  o = odds[1].find_all("a")
  ol = []
  for x in o[0].childGenerator():
    if str(type(x)) == "<class 'bs4.element.NavigableString'>":
      ol.append(str(x))
  ol1 = [x.replace(u"\xa0", " ") for x in ol[1:]]
  ol2 = [x.replace(u"\n\t\t\t\t\t\t\t", "") for x in ol1]
  for x in range(0, 2):
    if x == 0 and ol2[x][0] is not "-":
      d["Over/Under"] = ol2[x]
      d["Favorite"] = teams[1].text
      d["Underdog"] = teams[0].text
    if x == 1 and ol2[x][0] is not "-":
      d["Over/Under"] = ol2[x]
      d["Favorite"] = teams[0].text
      d["Underdog"] = teams[1].text

  d["Away"] = teams[0].text
  d["Home"] = teams[1].text
  d["Date/Time"] = a.find("span", {"class": "cellTextHot"}).text
  # d["Temperature"] = weatherd[d["Home"]]["Temperature"]
  # d["Wind"] = weatherd[d["Home"]]["Wind"]
  l.append(d)

sortedArray = sorted(
    l,
    key=lambda x: datetime.strptime(x['Date/Time'], '%m/%d %H:%M %p')
)


df = pandas.DataFrame(sortedArray)

fd = pandas.DataFrame(weatherd)
df
# fd
