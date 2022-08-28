from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, SessionNotCreatedException, TimeoutException, ElementClickInterceptedException
import pandas as pd
import time, os, re, random,json
import asyncio
from taskutils import check_followed, twitter_follow, youtube, twitch, telegram, get_frens
from datetime import datetime
from utils import bcolors, get_userdir


#twitter bot to reply to each tweet on a page and store the result in csv file
class TwitterBot:
    def __init__(self, driver, username='', password=''):
        self.username = username
        self.password = password
        self.driver = driver
        

    def login(self):
        self.driver.get("https://twitter.com/login")
        self.driver.implicitly_wait(4)
        #check if already logged in
        if 'home' in self.driver.current_url:
            print('Already logged in')
            return True
        try:
            self.driver.find_element(By.CSS_SELECTOR,"input[autocomplete='username']").send_keys(self.username+Keys.ENTER)
            self.driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(self.password+Keys.ENTER)
            self.driver.implicitly_wait(10)
        except NoSuchElementException:
            print("Error: NoSuchElementException")
            return False
        except InvalidArgumentException:
            print("Error: InvalidArgumentException")
            return False
        except SessionNotCreatedException:
            print("Error: SessionNotCreatedException")
            return False
        except TimeoutException:
            print("Error: TimeoutException")
            return False
        except ElementClickInterceptedException:
            print("Error: ElementClickInterceptedException")
            return False
        return True
    
    def open_tweet(self, url,rt=False):
        self.driver.get(url)
        print("opening",self.driver.title)
        self.driver.implicitly_wait(2)
        bottom_bar = self.driver.find_element(By.CSS_SELECTOR,"div.r-s1qlax[role='group']") #like,rt bar on bottom of a tweet
        rt_btn = bottom_bar.find_elements(By.CSS_SELECTOR,"div[role='button']")
        if len(rt_btn)==4:
            rt_btn = rt_btn[1]
        else:
            rt_btn = rt_btn[2]
        if rt_btn.get_attribute("data-testid") == "unretweet":
            print("already retweeted\n")
            return 'already RTed'
        else:
            bottom_bar.find_element(By.CSS_SELECTOR,"div[data-testid='like']").click() #like if not already liked
            rt_btn.click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR,"div[data-testid='retweetConfirm']").click() #click rt popup to confirm rt

    #reply to a tweet using url
    def reply(self, url, message, ss_counter):
        try:
            #self.driver.get(url)
            self.driver.implicitly_wait(2)
            #reply button
            self.driver.find_element(By.CSS_SELECTOR,"div[data-testid='reply']").click()
            #self.driver.find_element(By.CSS_SELECTOR, "div [aria-label='Reply']").click()
            self.driver.implicitly_wait(2)
            #message box
            message_box = self.driver.find_elements(By.CSS_SELECTOR,"div[role='dialog']")[1]
            if message!='' and ss_counter >= 0:
                message_box.find_element(By.CSS_SELECTOR,"div[aria-label='Tweet text']").send_keys(message)
                #upload ss
                upload_img = message_box.find_element(By.CSS_SELECTOR,"input[data-testid='fileInput']")
                for s in range(0,ss_counter):
                    upload_img.send_keys(os.getcwd()+f'/ss/{s}.png')
                    time.sleep(1)

            else:
                if message!='':
                    message_box.find_element(By.CSS_SELECTOR,"div[aria-label='Tweet text']").send_keys(message)
                elif ss_counter >= 0:
                    upload_img = message_box.find_element(By.CSS_SELECTOR,"input[data-testid='fileInput']")
                    for s in range(0,ss_counter):
                        upload_img.send_keys(os.getcwd()+f'/ss/{s}.png')
                        time.sleep(1)
            self.driver.implicitly_wait(2)
            message_box.find_element(By.CSS_SELECTOR,"div[data-testid='tweetButton']").send_keys(Keys.ENTER)

            #wait for message box to close
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR,"div[role='dialog']")))
            #time.sleep(4)
            return True
        except NoSuchElementException:
            print("Error: NoSuchElementException")
            return False
        except ElementClickInterceptedException:
            print("Error: ElementClickInterceptedException")
            return False

    def logout(self):
        try:
            self.driver.find_element_by_xpath("//button[@class='dropdown-link']").click()
            self.driver.find_element_by_xpath("//button[@class='dropdown-link']").click()
            self.driver.implicitly_wait(10)
        except NoSuchElementException:
            print("Error: NoSuchElementException")

    def close(self):
        self.driver.close()

    
class Tasks:
    def __init__(self, tweet_url, tasks, driver, twitter):
        self.tasks = json.loads(tasks)
        self.twitter = twitter
        self.tweet_url = tweet_url
        self.driver = driver
        self.tasks_done = False
        self.ss_counter = 0
        print(tasks)
    
    def do_tasks(self):
        try:
            #empty ss folder
            for the_file in os.listdir(os.getcwd()+'/ss/'):
                file_path = os.path.join(os.getcwd()+'/ss/', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(e)
            
            if self.tasks['rt']:
                self.twitter.open_tweet(self.tweet_url,rt=True)
            if self.tasks['follow']:
                for user in self.tasks['follow']:
                    if user == self.tasks['noti']:
                        if twitter_follow(self.driver, user, follow=True, noti=True, ss_index=self.ss_counter):
                            self.ss_counter += 1
                    else:
                        if not check_followed(user):
                            twitter_follow(self.driver, user, follow=True)
            
            if self.tasks['youtube']:
                time.sleep(2)
                for url in self.tasks['youtube'][0]:
                    if self.tasks['youtube'][1]:
                        #comment doesn't work
                        youtube(self.driver, url, comment=False, ss_index=self.ss_counter)
                    else:
                        youtube(self.driver, url, ss_index=self.ss_counter)
                    self.ss_counter += 1
            
            if self.tasks['twitch']:
                time.sleep(2)
                for url in self.tasks['twitch']:
                    twitch(self.driver, url, ss_index=self.ss_counter)
                    self.ss_counter += 1
            
            if self.tasks['telegram']:
                time.sleep(2)
                for url in self.tasks['telegram']:
                    telegram(self.driver, url, ss_index=self.ss_counter)
                    self.ss_counter += 1
            

            #forming reply message
            if self.tasks['tag'] or self.ss_counter>0:
                self.driver.implicitly_wait(2)
                if self.tasks['tag']:
                    message = get_frens(self.tasks['tag'])
                else:
                    message = ''
                self.twitter.reply(self.tweet_url, message, self.ss_counter)
            
            self.tasks_done = True
            return True
        except Exception as e:
            print(e)
            #timetamp for filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.driver.get_screenshot_as_file(f'error/{timestamp}.png')
            return False



def dateconvert(date):
    date = date.split('T')
    date = date[0].split('-')
    date = date[0]+date[1]+date[2]
    return int(date)


#main function
def twittermain(username='', password='', reply_text = "gl", csv_file = "tweets.csv", max_days_old=2):
    #add column tasks_done to csv if not exist
    df = pd.read_csv(csv_file)
    if 'tasks_done' not in df.columns:
        df['tasks_done'] = ''
        df.to_csv(csv_file, index=False)
    

    #initialize the driver and the twitter class
    options = webdriver.ChromeOptions()
    parser = ConfigParser()
    parser.read('config.ini')
    options = webdriver.ChromeOptions()
    args = json.loads(parser.get('chrome_options','args'))
    for arg in args:
        options.add_argument(arg)
    options.add_argument('--user-data-dir='+get_userdir())
    driver = webdriver.Chrome(options=options)
    try:
        twitter = TwitterBot(driver, username, password)
    except:
        driver.quit()
        print("Error: driver not initialized")
        exit()

    #login to twitter
    #twitter.login()

    #select tweet_url from csv where tasks_done is empty
    df = pd.read_csv(csv_file)
    #filters
    df1 = df[df['tasks_done'].isnull()]
    df1['tweet_date'] = df1['tweet_date'].apply(dateconvert)
    now = int(datetime.now().strftime("%Y%m%d"))
    df1 = df1[df1['tweet_date']>now-max_days_old]
    tweet_url_list = df1['tweet_url'].tolist()
    
    completed = 0
    for tweet_url in tweet_url_list:
        tasks = df[df['tweet_url'] == tweet_url]['tasks'].values[0]
        t1 = Tasks(tweet_url, tasks, driver, twitter)

        #update the tasks_done column
        tasks_done = t1.do_tasks()
        if tasks_done:
            df.loc[df['tweet_url'] == tweet_url, 'tasks_done'] = tasks_done
        else:
            #delete this row from df
            df = df[df['tweet_url'] != tweet_url]
        df.to_csv(csv_file, index=False)
        completed+=1
        print(bcolors.OKBLUE+'Progress: '+ bcolors.OKGREEN+str(completed) +bcolors.OKBLUE+ '/' + str(len(tweet_url_list))+bcolors.ENDC)

    #logout and close the driver
    time.sleep(2)
    #close the driver
    driver.quit()


twittermain()