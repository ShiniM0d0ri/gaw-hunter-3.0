import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random
from configparser import ConfigParser

def twitter_follow(driver,username, follow=True, noti=False, ss_index=0):
    driver.switch_to.new_window('tab')
    url = 'https:twitter.com/'+username.strip('@')
    driver.get(url)
    print("opening", driver.title)
    time.sleep(3)
    try:
        follow_btn = driver.find_element(By.CSS_SELECTOR,".css-1dbjc4n[data-testid='placementTracking'] div[role='button']")
        if follow_btn.text == "Follow":
            follow_btn.click()
        else:
            print("Already following")
        if noti:
            noti_btn = driver.find_element(By.CSS_SELECTOR,".css-1dbjc4n[data-testid='sendDMFromProfile'] ~ div div")
            if noti_btn.get_attribute("aria-label") != "Turn off Tweet notifications":
                try:
                    noti_btn.click()
                except:
                    print("fix this popup error")
            else:
                print("notification already on")
            time.sleep(2)
            driver.get_screenshot_as_file(f'ss/{ss_index}.png')
        time.sleep(3)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return False    

def youtube(driver, url, like=True, sub=True, comment=False, cmt="@vnchoudhary357\ngl everyone", ss_index=0):
    driver.switch_to.new_window('tab')
    driver.get(url)
    print("opening",driver.title)
    time.sleep(2)
    url = driver.current_url
    try:
        if 'watch' in url:
            if like:
                like_btn = driver.find_element(By.CSS_SELECTOR,"#menu-container button")
                if like_btn.get_attribute("aria-pressed") != "true":
                    print('liking the video')
                    like_btn.find_element(By.CSS_SELECTOR,"yt-icon").click()
                else:
                    print("already liked")
            if sub:
                sub_btn = driver.find_elements(By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-subscribe-button-renderer")[0]
                if sub_btn.text.strip() == "SUBSCRIBE":
                    print('subbing')
                    sub_btn.click()
                else:
                    print('already subbed')
            driver.execute_script("window.scrollTo(0, 500)")
            time.sleep(2)
            if comment:
                driver.find_element(By.ID, "placeholder-area").click()
                cmt_box = driver.find_element(By.ID, "contenteditable-root")
                cmt_box.send_keys(cmt)
                cmt_box.click()
                time.sleep(2)
                #driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = '"+cmt+"'}", cmt_box)
                driver.find_element(By.CSS_SELECTOR, "#submit-button #button").click()
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 500)")
        elif 'channel' in url or url.split("/")[3] == 'c':
            #sub the channel
            sub_btn = driver.find_element(By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-subscribe-button-renderer")
            if sub_btn.text.strip() == "SUBSCRIBE":
                print('subbing')
                sub_btn.click()
            else:
                print('already subbed')
        #time.sleep(3)
        driver.get_screenshot_as_file(f'ss/{ss_index}.png')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True

    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return False

def twitch(driver, url, follow=True, ss_index=0):
    driver.switch_to.new_window('tab')
    driver.get(url)
    print("opening",driver.title)
    time.sleep(5)
    #url = driver.current_url
    try:
        follow_btn = driver.find_elements(By.CSS_SELECTOR,"div[data-target=channel-header-right] button.ScCoreButton-sc-1qn4ixc-0")[0]
        if follow_btn.get_attribute("data-a-target") == "follow-button":
            follow_btn.click()
        elif follow_btn.get_attribute("data-a-target") == "unfollow-button":
            print("Already following...")
        time.sleep(3)
        driver.get_screenshot_as_file(f'ss/{ss_index}.png')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return False


def telegram(driver, url, ss_index=0):
    driver.switch_to.new_window('tab')
    driver.get(url)
    try:
        print("opening",driver.title)
        time.sleep(3)
        url = driver.current_url
        channel = url.split('/')[-1]
        print(channel)
        driver.get('https://web.telegram.org/?legacy=1#/im?p=@'+channel)
        print("opening",driver.title)
        time.sleep(3)
        try:
            join_btn = driver.find_element(By.CSS_SELECTOR,".im_edit_start_actions a")
            if join_btn.text == "+ JOIN":
                join_btn.click()
            else:
                print(join_btn.text)
        except NoSuchElementException:
            print("already joined tg")
        time.sleep(3)
        driver.get_screenshot_as_file(f'ss/{ss_index}.png')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return False

def get_frens(n):
    parser = ConfigParser()
    parser.read('config.ini')
    frens = parser.get('tags', 'friends').split(',')
    return " ".join(random.sample(frens,n))

def check_followed(user):
    with open('followed.txt','a+') as f:
        for line in f.readlines():
            if user in line:
                return True
        #add user to followed.txt
        f.write(user+'\n')
    return False