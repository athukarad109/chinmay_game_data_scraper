from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')

DRIVER_PATH = "D:\chromedriver-win32\chromedriver-win32\chromedriver"
# firefox = "D:\Firefox driver\geckodriver-v0.33.0-win32"
driver = webdriver.Chrome(options=options)


#TODOS - create function to fetch number of reviews and number of units sold - review to sales
#TODOS - graphs and stuff piechart maybe

#TODOS - create function to fetch top 5 reviews and publisher
def get_individual_data(link):
    driver.get(link)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    reviews_list = driver.find_elements(By.CLASS_NAME, "review_box   ")
    info = driver.find_element(By.ID, "genresAndManufacturer")
    publishers = info.find_elements(By.CLASS_NAME, "dev_row")
    review_section = driver.find_element(By.CLASS_NAME, "user_reviews_summary_row")
    review_count = driver.find_elements(By.CLASS_NAME, "responsive_hidden")


    publisher = ""

    for pub in publishers:
        item = pub.text.split(":")
        if item[0] == "PUBLISHER":
            publisher = (item[1])

    # all_reviews = []

    # review_count = 5
    # for review in reviews_list:
    #     if review_count <= 0:
    #         break
    #     reviewer_name = review.find_element(By.CLASS_NAME, "persona_name")
    #     this_review = review.find_element(By.CLASS_NAME, "content")
    #     all_reviews.append(f"{reviewer_name.text} : {this_review.text}")
    #     review_count -= 1

    return {"publisher": publisher, "reviews": review_section.text.split(":\n")[1]}
    

# print(get_individual_data('https://store.steampowered.com/app/311310/Naval_Action/'))


genre = input("Enter genre : ")

url = f"https://store.steampowered.com/search/?term={genre}"
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')

results_array = soup.find_all("div", id = "search_resultsRows")[0]

games = results_array.find_all('a')

game_sheet_headers = ['Sr. no', 'Name', 'price', 'realease date', 'publisher', 'Link', 'reviews']

game_sheet_data = []
game_dict = {}

i_ = []
name_ = []
price_ = []
dates_ = []
publisher_ = []
link_ = []
revs_ = []

i = 1
for game in games:
    link = game['href']
    name = game.find('span', {"class": "title"})
    price = game.find('div', {"class" : "discount_final_price"})
    release_date = game.find('div', {"class": "col search_released responsive_secondrow"}).text
    details = {}
    try:
        details = get_individual_data(link)
    except:
        details = {"publisher": "Failed to fetch", "reviews": "Failed to fetch"}

    publisher = details['publisher']
    revs = details['reviews']

    amt = 0.0

    if price:
        amt = float(price.text[1:].replace(',', ''))
    else:
        amt = 0.0

    # game_sheet_data.append([i, name.text, amt, release_date, publisher, link, revs])
    i_.append(i)
    name_.append(name.text)
    price_.append(amt)
    dates_.append(release_date)
    publisher_.append(publisher)
    link_.append(link)
    revs_.append(revs)


    game_dict = {'Sr. no' : i_, 'Name': name_, 'Price': price_, "Date": dates_, "publisher": publisher_, "Link to steam": link_, 'Reviews': revs_}
    i+=1


this_df = pd.DataFrame.from_dict(game_dict)
print(this_df)
this_df.to_csv(f"./Sheets/{genre}.csv")


# with open(f"./Sheets/{genre}.csv", "w") as file:
#     writer = csv.writer(file)
#     writer.writerow(game_sheet_headers)
#     writer.writerows(game_sheet_data)

