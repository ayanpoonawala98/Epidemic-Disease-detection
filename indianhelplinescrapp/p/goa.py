from selenium import webdriver
from bs4 import BeautifulSoup
import requests

#driver = webdriver.Chrome()

url= requests.get('https://indianhelpline.com/GOA/').text

#driver.get('https://indianhelpline.com/GOA/')

#html_doc = driver.page_source

soup = BeautifulSoup(url, 'lxml')
#print(soup.prettify)

table= soup.findAll('tr')
#print(table[42])

file =open('goa.csv','w')
header=' Name , Number\n'
file.write(header)
for td in table[42: ]:
    try:
        tr = td.findAll('td')
        name = tr[0].text
        number = tr[1].text
        print(name, number)
    except:
        pass
    
    file.write(name.replace(',','') + ',' + number.replace(',','|')+ '\n')
file.close()

