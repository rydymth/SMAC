import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import pandas as pd
import json
import os

# url = 'https://store.steampowered.com/category/hack_and_slash/'
url = 'https://store.steampowered.com/contenthub/querypaginated/tags/ConcurrentUsers/render/'

params = {
    "query": "",
    "start": 0,
    "count": 5,
    "cc": "US",
    "l": "english",
    "v": "4",
    "tag": "Action",
    "tagid": "19",
}


links = []
name = []
tags = []
for page in range(5):  # <-- increase number of pages here
    params["start"] = 15 * page
    data = requests.get(url, params=params).json()
    soup = BeautifulSoup(data["results_html"], "html.parser")
    for link in soup.find_all("a", href=True):
        links.append(link["href"])
    for item in soup.select(".tab_item_content"):
                name.append(item.select_one(".tab_item_name").text)
                tags.append(item.select_one(".tab_item_top_tags").text)

dd = {'name': name, 'tags': tags}
df = pd.DataFrame(dd)
df.to_csv("./game.csv")

print('Got web Pages')
linkList = []
appIDs = []
reviews = []
for i in links:
    linkList.append(i.split("/"))

for i in linkList:
    appIDs.append(int(i[4]))

for i in appIDs:
    strConcat = "https://steamcommunity.com/app/" + str(i) + "/reviews/?browsefilter=toprated&snr=1_5_100010_"
    reviews.append(strConcat)

print('Got Links')

for i in reviews:
    tmp = []
    data = requests.get(i).text
    soup = BeautifulSoup(data, 'html.parser')
    for j in soup.find_all('div', {'class': 'apphub_UserReviewCardContent'}):
        print('putting this is tmp')
        tmp.append(j.text)

    print('tmp data: \n', tmp,)
    print('length of current tmp: ', len(tmp))
    print('dumping json file')
    jsonD = json.dumps(tmp)
    fname = "./" + str(reviews.index(i)) + ".json"
    f = open(fname, "x") 
    with open(fname, "w") as outfile:
        outfile.write(jsonD)


