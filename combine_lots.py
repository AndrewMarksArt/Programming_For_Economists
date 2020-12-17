"""
Get data from data_files
    --> Phillips
        --> Lot_Details
            --> CSV_files
                --> batch_1

contains files with links to all auctions lots from the
all_sales_auction_list.csv

combine the links into one list
"""


# imports
import os
import time
import numpy as np
import pandas as pd

from CONFIG import config
from UTILS import utils


# function to create a random wait time
def rand_wait(min_time=1, max_time=3):
    wait = np.random.randint(min_time, max_time)
    time.sleep(wait)


def get_details(lot_link):
    details = []
    try:
        artist = driver.find_element_by_class_name("lot-page__lot__maker__name").text
    except:
        artist = "cant find artist name"

    try:
        title = driver.find_element_by_class_name("lot-page__lot__title").text
    except:
        title = "cant find title"

    try:
        add_info = driver.find_element_by_class_name("lot-page__lot__additional-info")
        add_info = add_info.find_elements_by_tag_name("span")
        year_made = add_info[0].text
        medium = add_info[1].text
        size = add_info[-1].text
    except:
        year_made = "cant find year_made"
        medium = "cant find medium"
        size = "cant find size"

    try:
        estimate = driver.find_element_by_class_name("lot-page__lot__estimate").text
        estimate = estimate.split()[1:4:2]
    except:
        estimate = "cant find estimate"

    try:
        sold_for = driver.find_element_by_class_name("lot-page__lot__sold").text
        sold_for = sold_for.split()[-1]
    except:
        sold_for = "not sold or cant find sale price"

    try:
        sale_info = driver.find_element_by_class_name("sale-title-banner__link")
        sale_info = sale_info.find_elements_by_tag_name("h3")
        sale_info = sale_info[-1].text.split()
    except:
        sale_info = "cant find sale location"


    try:
        image = driver.find_element_by_class_name("phillips-image__image")
        image = image.get_attribute("src")
    except:
        image = "cant find image or image url"

    url = lot_link

    details.extend(
        [artist, title, year_made, medium, size, estimate, sold_for, sale_info, image, url]
    )

    return details


# initialize list that will hold all links to auction lots
all_lots = []
# set path to files that contain links to lots from auctions
path = config.PHILLIPS_LOTS_CSV+'batch_1/'

# loop through files and get all the links to auction lots,
# append them to the all_lots list
for filename in os.listdir(path):
    if filename.endswith(".txt"):
        with open(path+filename, 'r') as f:
            lines = [line.strip() for line in f]
            for line in lines:
                all_lots.append(line)
        continue
    else:
        continue

# initialize the selenium chrome driver
driver = utils.start_browser(config.CHROME_PATH)
# initialize a WebDriverUtilities object
browser = utils.WebDriverUtilities(driver)

"""driver.get(all_lots[0])
print("Current session is {}".format(driver.session_id))
rand_wait()
driver.get(all_lots[1])
print("Current session is {}".format(driver.session_id))
rand_wait()
driver.get(all_lots[2])
print("Current session is {}".format(driver.session_id))
rand_wait()
driver.get(all_lots[3])
print("Current session is {}".format(driver.session_id))
rand_wait()
driver.get(all_lots[4])
print("Current session is {}".format(driver.session_id))"""
all_lot_details = []

for i in range(len(all_lots)):
    driver.get(all_lots[i])
    rand_wait()
    if i == 0:
        browser.close_cookies()
        rand_wait()
    else:
        pass

    temp = get_details(all_lots[i])
    all_lot_details.append(temp)


    """artist = driver.find_element_by_class_name("lot-page__lot__maker__name").text
    title = driver.find_element_by_class_name("lot-page__lot__title").text
    add_info = driver.find_element_by_class_name("lot-page__lot__additional-info")
    add_info = add_info.find_elements_by_tag_name("span")
    year_made = add_info[0].text
    medium = add_info[1].text
    size = add_info[-1].text
    estimate = driver.find_element_by_class_name("lot-page__lot__estimate").text
    estimate = estimate.split()[1:4:2]
    sold_for = driver.find_element_by_class_name("lot-page__lot__sold").text
    sold_for = sold_for.split()[-1]
    sale_info = driver.find_element_by_class_name("sale-title-banner__link")
    sale_info = sale_info.find_elements_by_tag_name("h3")
    sale_info = sale_info[-1].text.split()
    image = driver.find_element_by_class_name("phillips-image__image")
    image = image.get_attribute("src")
    print(i, image)"""

driver.close()

data = pd.DataFrame(all_lot_details)
data.to_csv(config.PHILLIPS + "test_run.csv", index=False)
