from urllib.request import build_opener, HTTPCookieProcessor
import sys
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver


def get_data(tdclass):
    list = str(tdclass).replace("\t","").split('\n')
    for line in list:
        if(line.find("<") == -1 and line.strip() != ""):
            return line.strip()


def get_location(tdclass):
    loc = tdclass.find("a", class_="locationtip").text
    return loc

def get_date(tdclass):
    date = tdclass.find("a", class_="deadlinetip").text
    return date

def get_class_data(classNum):
    url = "https://webapp4.asu.edu/catalog/myclasslistresults?t=2197&k=" +classNum + "&k=" + classNum + "&hon=F&promod=F&e=all&page=1"
    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    catalog = soup.find("table",{'id':'CatalogList'})

    courseCode = get_data(catalog.find_all("td", class_="subjectNumberColumnValue nowrap"))
    coursename = get_data(catalog.find_all("td", class_="titleColumnValue"))
    instructor = get_data(catalog.find_all("td", class_="instructorListColumnValue"))
    daysList = get_data(catalog.find_all("td", class_="dayListColumnValue hide-column-for-online"))
    start = get_data(catalog.find_all("td", class_="startTimeDateColumnValue hide-column-for-online"))
    end = get_data(catalog.find_all("td", class_="endTimeDateColumnValue hide-column-for-online"))
    location = get_location(catalog.find("td", class_="locationBuildingColumnValue nowrap"))
    dates = get_date(catalog.find("td", class_="startDateColumnValue nowrap"))


    classInfo = {
                'courseCode':courseCode,
                'courseName' : coursename,
                'instructor':instructor,
                'days': daysList,
                'start': start,
                'end':end,
                'location':location,
                'dates':dates
    }
    print(classInfo)



get_class_data(sys.argv[1])
