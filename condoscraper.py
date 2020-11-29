from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import cloudscraper
import re
import json
import csv

totaldata = []


def geturl(driver):
    elements = driver.find_element_by_css_selector("div[class^='listing-card listing-id']")
    elements.click()
    print(driver.current_url)
    return driver.current_url

def driverr(driverpath):
    options = Options()
    user_agent = 'I LIKE CHOCOLATE'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=driverpath,options=options)
    url = "https://www.ddproperty.com/en/condo-for-sale"
    driver.get(url)
    url = geturl(driver)
    info = sourcescrape(url)
    totaldata.append(info)
    driver.quit()



def sourcescrape(url):
    t=[-1]*7
    gym = False
    parking = False
    pool = False
    library = False
    club = False
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url).content
    soup = BeautifulSoup(page, 'lxml')
    condoName = "ND"
    address = "ND"
    price = "ND"
    try:
        condoName = soup.find("meta",  property="og:title")["content"]
    except:
        print("no name")
    try:
        address = soup.find("span", itemprop="streetAddress").get_text()
    except:
        print("no address")
    try:
        price = soup.find("span", class_="price-value").get_text()
    except:
        print("no price")
    t[0] = price
    room = None
    bath = None
    size = None

    try:
        bar = soup.find_all("span", class_="element-label")
        room = bar[2].get_text().strip()
        bath = bar[3].get_text().strip()
        size = bar[4].get_text().strip()
    except:
        print("no data")


    try:
        facil = soup.find_all("span", itemprop="name")
        for fac in facil:
            if (fac.get_text()=="Library"):
                library=True
            if (fac.get_text() == "Covered car park" or fac.get_text() == "Open car park"):
                parking=True
            if (fac.get_text() == "Swimming pool"):
                pool=True
            if (fac.get_text() == "Fitness corner" or fac.get_text() == "Gymnasium room"):
                gym=True
            if (fac.get_text() == "Clubhouse"):
                club=True
    except:
        gym = None
        parking = None
        pool = None
        library = None
        club = None
        print("no data")

    pricearr = []
    try:
        data = soup.find_all("script", type="text/javascript")[1].string
        p = re.compile('var guruApp = (.*);')
        m = p.search(data)
        dd = json.loads(m.groups()[0])
        alldata = dd["priceInsightsWidgetData"]["priceInsightPropertyValueTab"]["sale"]["half-yearly"]["1"]["data"]
        for d in alldata:
            pricearr.append(d[1])
        index=1
        while(len(pricearr)>0):
            t[index]=pricearr.pop(0)
            index+=1
    except:
        print("no data")


    # print(condoName)
    # print(address)
    # print(gym)
    # print(parking)
    # print(pool)
    # print(library)
    # print(club)
    # for x in t:
    #     print(x)

    unit = {"condoName": condoName, "address": address, "price": price, "t0":t[0],"t1":t[1],"t2":t[2],"t3":t[3],"t4":t[4],"t5":t[5],"t6":t[6],"room":room,"bath":bath,"size":size, "gym":gym,"parking":parking,"pool":pool,"library":library,"club":club}
    print(unit)
    return unit

print("Enter chromedriver path (use / not \): ")
path = input()
print("Enter filename (do not include extension)")
name = input()
filename=name+".csv"
for x in range(100):
    print(x)
    driverr(path)

f = open(filename, "w", encoding='utf-8-sig')
writer = csv.DictWriter(
    f, totaldata[0].keys())
writer.writeheader()
writer.writerows(totaldata)
print("PROCESS COMPLETED")
f.close()