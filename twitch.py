# pylint: disable=missing-docstring,invalid-name
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import chromedriver_binary
import json 

#number of sub posing problem
def get_general_infos(url, driver):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"content-wrapper\"]")))
    nbr_followers = int(driver.find_element(By.CSS_SELECTOR, "li.list-group-item:nth-child(4) > div:nth-child(1) \
                                            > div:nth-child(2) > span:nth-child(2)").text.replace(",", ""))
    nbr_subs = int(driver.find_element(By.CSS_SELECTOR, "div.g-x-wrapper:nth-child(6) > div:nth-child(1) > div:nth-child(2) \
        > div:nth-child(1) > div:nth-child(1)").text.replace(",", ""))
    return nbr_followers, nbr_subs

def get_followers_infos(url, driver):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"content-wrapper\"]/div[3]")))
    last_month_foll = int(driver.find_element(By.CSS_SELECTOR, "#DataTables_Table_1 > tbody:nth-child(2) > tr:nth-child(1) \
                                              > td:nth-child(3)").text.replace(".","").replace("M", "0000"))

    snd_last_month_foll = int(driver.find_element(By.CSS_SELECTOR, "#DataTables_Table_1 > tbody:nth-child(2) > tr:nth-child(2) \
                                                  > td:nth-child(3)").text.replace(".","").replace("M", "0000"))

    thrird_last_month_foll = int(driver.find_element(By.CSS_SELECTOR, "#DataTables_Table_1 > tbody:nth-child(2) > tr:nth-child(3) \
                                                     > td:nth-child(3)").text.replace(".","").replace("M", "0000"))
    return last_month_foll, snd_last_month_foll, thrird_last_month_foll

def get_subscribers_infos(url, driver):
    # number of subs last 3 months subs
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"content-wrapper\"]/div[5]")))

    last_month_sub = int(driver.find_element(By.CSS_SELECTOR, "#subscribers > tbody > tr:nth-child(2) > td:nth-child(2) \
                                             > b").text.replace(",",""))
    snd_last_month_sub = int(driver.find_element(By.CSS_SELECTOR, "#subscribers > tbody > tr:nth-child(3) > td:nth-child(2) \
                                                 > b").text.replace(",",""))
    third_last_month_sub = int(driver.find_element(By.CSS_SELECTOR, "#subscribers > tbody > tr:nth-child(4) > td:nth-child(2) \
                                                   > b").text.replace(",",""))
    return last_month_sub, snd_last_month_sub, third_last_month_sub

def get_streams_infos(url, driver):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"content-wrapper\"]/div[3]")))

    last_stream_avg_views = int(driver.find_element(By.CSS_SELECTOR, "tr.odd:nth-child(1) > td:nth-child(3) \
                                                    > span:nth-child(1)").text.replace(",", ""))
    snd_last_stream_avg_views = int(driver.find_element(By.CSS_SELECTOR, "tr.even:nth-child(2) > td:nth-child(3) \
                                                        > span:nth-child(1)").text.replace(",", ""))
    third_last_stream_avg_views = int(driver.find_element(By.CSS_SELECTOR, "tr.odd:nth-child(3) > td:nth-child(3) \
                                                          > span:nth-child(1)").text.replace(",", ""))
    return last_stream_avg_views, snd_last_stream_avg_views, third_last_stream_avg_views
    

def twitch(creator):
    twitch_general = f'https://twitchtracker.com/{creator}'
    twitch_streams = f'https://twitchtracker.com/{creator}/streams'
    twitch_subs = f'https://twitchtracker.com/{creator}/subscribers'
    twitch_stats = f'https://twitchtracker.com/{creator}/statistics'
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=OFF")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    nbr_followers, nbr_subs = get_general_infos(twitch_general, driver)
    last_month_foll, snd_last_month_foll, thrird_last_month_foll = get_followers_infos(twitch_stats, driver)
    foll_growth_rate = round(((last_month_foll/ thrird_last_month_foll)**(1/3) - 1) * 100, 2)
    last_month_sub, snd_last_month_sub, third_last_month_sub = get_subscribers_infos(twitch_subs, driver)
    subs_growth_rate = round(((nbr_subs/ snd_last_month_sub)**(1/3) - 1) * 100, 2)
    last_stream_avg_views, snd_last_stream_avg_views, third_last_stream_avg_views = get_streams_infos(twitch_streams, driver)
    three_last_streams_avg_views = int((last_stream_avg_views + snd_last_stream_avg_views + third_last_stream_avg_views) / 3)
    driver.quit()
    values = {
    "current # of followers" : nbr_followers,
    "# of followers of last month " : last_month_foll,
    "# of followers 2 months ago" :  snd_last_month_foll,
    "# of followers 3 months ago" : thrird_last_month_foll,
    "Avg growth rate of new followers (%)" : foll_growth_rate,
    "current # of subscribers" : nbr_subs,
    "# of subscribers of last month " : last_month_sub,
    "# of subscribers 2 months ago" :  snd_last_month_sub,
    "# of subscribers 3 months ago" : third_last_month_sub,
    "Avg growth rate of new subscribers on 3 last months (%)" : subs_growth_rate,
    "Avg CCr views on last stream" : last_stream_avg_views,
    "Avg CCr views on second last stream" : snd_last_stream_avg_views,
    "Avg CCr views on third last stream" : third_last_stream_avg_views,
    "Av. # of viewers on 3 last streams" : three_last_streams_avg_views
    }
    return values # json.dumps(values) #, indent = 4

print(twitch("pokimane"))
