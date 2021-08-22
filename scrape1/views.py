from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time
from django.db import connection,transaction
from scrape1.models import scrapeData

# Create your views here.
cursor = connection.cursor()
def scrape_data():
    url = "https://news.google.com/search?q=nri&hl=en-IN&gl=IN&ceid=IN%3Aen/"

    content = requests.get(url)
    htmlContent = content.content

    soup = BeautifulSoup(htmlContent, 'html.parser')

    title = soup.find_all("a", class_ = "DY5T1d RZIKme")
    titleList = []
    linksList = []

    for tit in title:
        titleList.extend(tit.contents)
        linksList.append("https://news.google.com/"+tit["href"][2:])

    pub_time = soup.find_all("time", class_ = "WW6dff uQIVzc Sksgp")
    timeList = []

    for tim in pub_time:
        timeList.extend(tim.contents)

    dbTitle = []
    for u in scrapeData.objects.all():
        dbTitle.append(u.dataTitle)

    for i in range(len(titleList)):
        if titleList[i] not in dbTitle:
            sql = 'INSERT into scrapeData(dataTitle,dataTime,dataLink)values("%s","%s","%s")'%(titleList[i], timeList[i], linksList[i])
            cursor.execute(sql)

    transaction.commit()
    return "done"

def retrieveData(request):
    done = scrape_data()
    if done == "done":
        data = scrapeData.objects.all()
        return render(request, "index.html", {"data":data})
    

    
