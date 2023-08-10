import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json

class Data:
    def __init__(self,name,releaseyear,certificate,duration,genre,rating,director,cast):
        self.name = name
        self.releaseyear = releaseyear
        self.certificate = certificate
        self.duration = duration
        self.genre = genre
        self.rating = rating
        self.director = director
        self.cast = cast
        
    def getName(self):
        print(self.name)
    def getReleaseYear(self):
        print(self.releaseyear)
    def getCertificate(self):
        print(self.certificate)
    def getDuration(self):
        print(self.duration)
    def getGenre(self):
        print(self.genre)
    def getRating(self):
        print(self.rating)
    def getDirector(self):
        print(self.director)
    def getCast(self):
        print(self.cast)
    def getData(self):
        print(self.name,end=' | ')
        print(self.releaseyear,end=' | ')
        print(self.certificate,end=' | ')
        print(self.duration,end=' | ')
        print(self.genre,end=' | ')
        print(self.rating,end=' | ')
        print(self.director,end=' | ')
        print(self.cast)


name = []
releaseyear = []
certificate = []
duration = []
genre = []
stars = []
director = []
cast = []
dir_and_act = []
rating_bar = ""
url = "https://www.imdb.com/search/title/?title_type=feature&countries=in&sort=alpha,asc&count=250"


for index in range(1,53270,250):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    url_path = soup.find('a',class_="lister-page-next")
    if url_path is not None:
        url = 'https://www.imdb.com/' + url_path['href']
    content = soup.find_all(class_='lister-item-content')
    header = soup.find_all(class_='lister-item-header')
    details = [c.find('p',class_='text-muted') for c in content]
    for c in content:
        ratingbar = c.find(class_="ratings-bar")
        if ratingbar is not None:
            r = ratingbar.find("div",class_='ratings-imdb-rating')
            if r is not None:
                r = r.find('strong')
                if r is not None:
                    stars.append(r.get_text())
                else:
                    stars.append("*")
            else:
                stars.append("*")
        else:
            stars.append("*")

    for c in content:
        p_elements = c.find_all('p')
        for p in p_elements:
            if not p['class']:
                if p is not None:
                    dir_and_act.append(p.get_text())
                else:
                    dir_and_act.append('empty')


    for h in header:
        name.append(h.find('a').get_text())
        temp = h.find('span',class_='lister-item-year').get_text()
        match = re.search("\d{4}",temp)
        if match is not None:
            match = match.group(0)
            if match:
                releaseyear.append(match)
        else:
            releaseyear.append("----")

    for d in details:
        c = d.find(class_='certificate')
        if c is not None:
            certificate.append(c.get_text())
        else:
            certificate.append("NA")
        r = d.find(class_='runtime')
        if r is not None:
            duration.append(r.get_text())
        else:
            duration.append("--:--")
        g = d.find(class_='genre')
        if g is not None:
            genre.append(g.get_text().strip("\n "))
        else:
            genre.append("____")

    for t in dir_and_act:
        str = re.split(r'Directors?:',t)[-1].split("|")[0].strip()
        str = re.sub(r'\n', '', str)
        director.append(str)
        str = re.split(r"Stars?:",t)[-1].strip()
        str = re.sub(r'\n','',str)
        cast.append(str)
    if url is None:
        break



obj = []
print(len(name))
for i in range(len(name)):
    obj.append(Data(name[i],releaseyear[i],certificate[i],duration[i],genre[i],stars[i],director[i],cast[i]))


json_data = json.dumps([o.__dict__ for o in obj], indent=4)

json_filename = "data.json"
with open(json_filename, 'w') as file:
    file.write(json_data)


data = [[o.name,o.releaseyear,o.certificate,o.duration,o.genre,o.rating,o.director,o.cast] for o in obj]
df = pd.DataFrame(data, columns=["name", "release year", "certificate", "duration", "genre", "rating", "director", "cast"])

excel_filename = "data.xlsx"
df.to_excel(excel_filename, index=False)




