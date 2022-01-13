import re
from selenium.webdriver.common.by import By
from setup import clear


def clean_text(text):
    text = text.lower()
    text = re.sub("#", "", text) #remove hashtags
    return text


def giveaway_check(text):
    if bool(re.search('(\$\d+)|(giveaway)|(\d+\$)|(giving)', text)) and not bool(re.search('(coingecko)|(coinmarketcap)|(gleam.io)',text)): #what should and should not be in a tweet
        return True
    else:
        return False

def get_follows(tweet_link,text):
    user = '@'+tweet_link.split('/')[-3].lower() #id of person who tweeted
    ids = re.findall('@\w+',text)
    if user not in ids:
        ids.append(user)
    return ids
    
def tagfren(text):
    n=0
    result = re.search('tags?\s\w+\s', text).group().split(' ')
    if result[1][0]=="a" or result[1][0]=="o":
        n=1
    elif result[1][0]=="y" or result[1][0]=="f" or result[1][0]=="s" or result[1][0]=="t":
        n=2
    else:
        n=int(result[1][0])
    return n

def get_tasks(text, text_element,tweet_link):
    tasks = {
            "rt": None, "like": None, "follow": [], "noti": None, "tag": None, 
            "youtube": [], "instagram": [], "telegram": [], "twitch": []
            }

    stream = bool(re.search('\sstream\s', text))
    
    if bool(re.search('(retweet)|(rt)|(ends\sin)|(\d+\$)|(\$\d+)', text))and not stream:
        tasks["rt"] = True
        tasks["like"] = True
        tasks["follow"] = get_follows(tweet_link, text)
        if 'notification' in text:
            tasks["noti"] = '@'+tweet_link.split('/')[-3].lower() #id of person who tweeted
        if bool(re.search('tags?\s\w+\s', text)):
            tasks["tag"] = tagfren(text)

        yt_urls = []
        yt_cmt = 0
        for j in text_element.find_elements(By.CSS_SELECTOR,"a"):
            if 'youtu' in j.text: #for both youtube.com and youtu.be
                yt_urls.append(j.get_attribute('href'))
                if 'comment' in text:
                    yt_cmt = 1
            elif 'instagram' in j.text:
                tasks["instagram"].append(j.get_attribute('href'))
            elif 'twitch.tv' in j.text:
                tasks["twitch"].append(j.get_attribute('href'))
            elif 't.me' in j.text:
                if 'joinchat' not in j.text:
                    tasks["telegram"].append(j.get_attribute('href'))
        tasks["youtube"].append(yt_urls)
        if yt_cmt:
            tasks["youtube"].append('comment')
        else:
            tasks["youtube"].append('')

    else:
        tasks["rt"] = False
    return tasks

#add colors class
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#get chrome user directory to be used
def get_userdir():
    import os
    parent_userdir = f"C:\\Users\{os.getlogin()}\AppData\Local\Google\Chrome\\User Data\\"
    userdir = f"C:\\Users\{os.getlogin()}\AppData\Local\Google\Chrome\\gaw\\"
    #copy parent_userdir contents to userdir
    if not os.path.exists(userdir):
        print(f"{bcolors.OKGREEN}Copying user data from {parent_userdir} to {userdir}{bcolors.ENDC}")
        cmd = f"Xcopy /E /I /C '{parent_userdir}' '{userdir}'"
        os.system(f"powershell.exe {cmd}")
        clear()
    
    return userdir
