"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from epidemicpred.views import home,contact,helpline,about,SearchResultsView,TweetView,sentiment,mapview,new,TableView,StateResultsView,pred,covid,job
import schedule,time
import pandas as pd
import numpy as np
import ast
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import os
import numpy as np
import matplotlib.pyplot as plt
import time,datetime
import os
import schedule
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import re
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('helpline/',helpline,name='helpline'),
    path('sentiment/',sentiment,name='sentiment'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('tweet/', TweetView.as_view(), name='search_results2'),
    path('map/',mapview,name='map'),
    path('pred/',pred,name='pred'),
    path('covid/',covid,name='covid'),
    path('new/',new,name='new'),
    path('tableview/',TableView.as_view(),name='Tableview'),
    path('state_result/', StateResultsView.as_view(), name='state_result'),


]
def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())




def job():
    today = datetime.datetime.now().date()
    x = str(today)
    y = str(today - datetime.timedelta(days=1))
    dengue ='twint -s "#dengue" --until '+x+' --since '+y+' --location --near INDIA --translate -l english --verified -o data/dengue.csv --csv'
    influ = 'twint -s "#influenza" --until '+x+' --since '+y+' --location --near INDIA --translate -l english --verified -o data/indluenza2018.csv --csv'
    malaria ='twint -s "#malaria" --until '+x+' --since '+y+' --location --near INDIA --translate -l english --verified -o data/malaria.csv --csv'
    covid = 'twint -s "#corona #covid-19" --until '+x+' --since '+y+' --location --near INDIA --translate -l english --verified -o data/covid.csv --csv '
    names = [dengue,influ,malaria,covid]
    for  name in names:
        print(name+' over /n/n/n/n/n/n')
        os.system(name)
    names = ["data/dengue.csv","data/indluenza2018.csv", "data/malaria.csv","data/covid.csv"]

    final_data_csv = pd.DataFrame(columns = ["",'date','tweet','hashtags','place'])
    print(124124)
    for name in names:
        data = pd.read_csv(name)
        sample = data.loc[:,['date','tweet','hashtags','place']]
        #sample.to_csv(name.split('.')[0] + "Final.csv", index = False)
        final_data_csv = pd.concat([final_data_csv, sample], axis = 0,sort=False)
    final_data_csv.to_csv("data/Final_data.csv", index = False)
    name = pd.read_csv("data/name.csv")
    print(2342)
    name = name.dropna(how = 'all')
    lst_city = [x.split('[')[0] for x in name[' City ']]
    lst_state = [x for x in name[' State']]
    data = pd.read_csv("data/Final_data.csv").values
    for i in range(data.shape[0]):
        data[i][3] = np.random.choice(lst_city)
    pd.DataFrame(data).to_csv("data/Final_data_with_location.csv", index = False)
    data = pd.read_csv("data/Final_data_with_location.csv")
    data['state'] = 'NaN'
    data = data.values
    for i in range(data.shape[0]):
        index = lst_city.index(data[i][3])
        data[i][4] = lst_state[index]
    pd.DataFrame(data).to_csv("data/Final_data_with_location.csv", index = False)
    data = pd.read_csv('data/Final_data_with_location.csv')
    data['polarity'] = 'NaN'
    data = data.values

    for i in range(data.shape[0]):
        text = data[i][1]
        analysis = TextBlob(clean_tweet(data[i][1]), analyzer=NaiveBayesAnalyzer())
        pol = analysis.sentiment.classification
        print(pol)
        data[i][5] = pol

    data = pd.DataFrame(data)
    data.rename(columns = {
            '0': "date",
            '1': "tweet",
            '2': "hashtags",
            '3': "city",
            '4': "state",
            '5': "polarity"
            }, inplace = True)
    data.to_csv("data/data.csv")


# def call():
#     print(2)
#
#     print(22)
#     schedule.every().day.at("00:00").do(job)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# call()
