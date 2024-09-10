from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome()

driver.get("https://www.imdb.com/chart/top/")

soup = BeautifulSoup(driver.page_source, "html.parser")

mov_data = []

mov_names = soup.find("ul",class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 dHaCOW compact-list-view ipc-metadata-list--base")

for movie in mov_names:
    h3_tag = movie.find('h3') 
    movie_year = movie.find("div", class_="sc-b189961a-7 btCcOY cli-title-metadata")
    rating = movie.find("div",class_="sc-e2dbc1a3-0 jeHPdh sc-b189961a-2 bglYHz cli-ratings-container")  
  
    if movie_year:
        first_div = movie_year.find('span')
    if rating:
        second_div = rating.find('span')
    
    print(f"Movie name: {h3_tag.text} Year: {first_div.text} Rating: {second_div.text}")
    
    dic = {
        "Movie": h3_tag.text,
        "Year": first_div.text,
        "Rating": second_div.text
    }
    
    mov_data.append(dic)
    
    df = pd.DataFrame(mov_data)
    df.to_csv("MovieData.csv",index=False)
    
    
time.sleep(20)
driver.quit()
