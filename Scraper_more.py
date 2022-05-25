from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL="https://exoplanets.nasa.gov/exoplanet-catalog/"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers=["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_period", "eccentricity"]
planet_data=[]
new_planet_data=[]

def scrape():
    for i in range(0,489):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        print("I am on page:" + str(i))
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            #print("I am saving the table on this page")
            li_tags = ul_tag.find_all("li")
            temp_list=[]
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            #print(planet_data[0][5])
        
def scrape_more_data(hyperlink):
    page=requests.get(hyperlink)
    soup=BeautifulSoup(page.content, "html.parser")
    for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
        td_tags=tr_tag.find_all("td")
        temp_list=[]
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
            except:
                temp_list.append("")
    new_planet_data.append(temp_list)

scrape()

for index, data in enumerate(planet_data):
    scrape_more_data(data[5])

final_planet_data=[]
for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data[index])
    print("adding data to row number: ", index)
    
with open("final_fresh.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)

print("Written the file")