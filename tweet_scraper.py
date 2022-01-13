from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidArgumentException, SessionNotCreatedException
import time
import re, json
import os
import sys
import datetime
import pandas as pd
import numpy as np
from configparser import ConfigParser
from utils import clean_text, giveaway_check, get_tasks,get_userdir
from chromedriver import get_driver


#get n number of tweets from a search query and scroll to get more and save them to a csv file
def get_tweets(query, n, driver,no_new_cap=5):
    count = 0
    count_no_new = 0
    #open twitter
    if query.startswith('http'):
        driver.get(query)
    elif query=='home':
        driver.get('https://twitter.com/home')
    elif query=='topics':
        driver.get('https://twitter.com/i/topics/10045347491')
    else:
        driver.get(f"https://twitter.com/search?q=min_retweets%3A10%20{query}&src=typed_query&f=live")
    #wait for results to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1dbjc4n[data-testid='tweet']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
    time.sleep(5)
    while(count<n):
        tweets = driver.find_elements(By.CSS_SELECTOR,".css-1dbjc4n[data-testid='tweet']")
        #get tweets
        for tweet in tweets:
            try:
                tweet_urls = tweet.find_elements(By.CSS_SELECTOR,"a[dir='auto']")
                for i in tweet_urls:
                    if 'status' in i.get_attribute('href'):
                        tweet_url = i.get_attribute('href')
                        break
            except Exception as e:
                driver.save_screenshot('error.png')
                print('tweet url not found'+str(e))
                continue
            print(tweet_url)
            #increment count if tweet_url value is not already in the tweets.csv file
            df = pd.read_csv('tweets.csv')
            if tweet_url not in df['tweet_url'].values:
                count+=1
                print(count)
                if count >= n:
                    break
            else:
                count_no_new+=1
                print(count_no_new,no_new_cap)
                if count_no_new >= no_new_cap:
                    return
                continue
            try:
                #for light theme
                #wait for text to load
                WebDriverWait(tweet, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-901oao.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0")))
                # check if tweet text element is present
                text_ele = tweet.find_element(By.CSS_SELECTOR,".css-901oao.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0")

            except NoSuchElementException:
                driver.save_screenshot('error.png')
                print("text_ele not found")
                continue
            except TimeoutException:
                driver.save_screenshot('error.png')
                print("Timed out waiting for text to load")
                continue
            #get tweet text
            tweet_text = text_ele.text
            #check if tweet is a giveaway
            text = clean_text(tweet_text)
            giveaway = giveaway_check(text)
            if giveaway:
                tasks = get_tasks(text, text_ele, tweet_url)
            else:
                continue
            #get tweet date
            tweet_date = driver.find_element(By.CSS_SELECTOR,"time").get_attribute('datetime')
            #bottom bar of a tweet
            bottom_bar = tweet.find_element(By.CSS_SELECTOR,"div.css-1dbjc4n.r-1ta3fxp.r-18u37iz.r-1wtj0ep.r-1s2bzr4.r-1mdbhws") #like,rt bar on bottom of a tweet
            #get tweet likes count
            tweet_likes = bottom_bar.find_elements(By.CSS_SELECTOR,"div[role='button']")[2].text
            #get tweet retweets count
            tweet_retweets = bottom_bar.find_elements(By.CSS_SELECTOR,"div[role='button']")[1].text
            #get tweet replies count
            tweet_replies = bottom_bar.find_elements(By.CSS_SELECTOR,"div[role='button']")[0].text
            #save the tweets to a csv file using pandas
            df = pd.DataFrame(data=[[tweet_url,tweet_text, tweet_date, tweet_retweets, tweet_likes, tweet_replies, giveaway, json.dumps(tasks),'']], columns=['tweet_url','tweet_text', 'tweet_date', 'tweet_retweets', 'tweet_likes', 'tweet_replies', 'giveaway', 'tasks', 'tasks_done'])
            df.to_csv('tweets.csv', mode='a', header=False, index=False)
            #close the tweet tab

        #scroll down to the last tweet element and wait for it to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1dbjc4n[data-testid='tweet']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()

    print(str(n)+" tweets added to tweets.csv")



def tweet_scraper(query='csgo giveaway', n=10, userdir= '', no_new_cap=5):
    parser = ConfigParser()
    parser.read('config.ini')
    options = webdriver.ChromeOptions()
    args = json.loads(parser.get('chrome_options','args'))
    for arg in args:
        options.add_argument(arg)  

    #set the user directory
    userdir = parser.get('SCRAPE', 'userdir')
    options.add_argument(f'--user-data-dir={get_userdir()}')
    #initialize driver
    try:
        driver = webdriver.Chrome(options=options)
    except InvalidArgumentException:
        print("User data directory is already in use\nClose all chrome windows or define another user directory")
        exit()
    except SessionNotCreatedException as e:
        print(str(e))
        print("Checking for chromedriver upate")
        d = get_driver()
        d.get("https://www.google.com")
        exit()
    #check if followed.txt is empty
    if os.stat('followed.txt').st_size == 0:
        input('Configure browser and press enter to continue')
    columns=['tweet_url','tweet_text', 'tweet_date', 'tweet_retweets', 'tweet_likes', 'tweet_replies', 'giveaway', 'tasks', 'tasks_done']
    #add columns to the csv file if they don't already exist
    if not os.path.exists('tweets.csv'):
        df = pd.DataFrame(columns=columns)
        df.to_csv('tweets.csv', index=False)
    
    
    #get the tweets
    get_tweets(query, n, driver,no_new_cap)
    #close the browser
    driver.quit()
