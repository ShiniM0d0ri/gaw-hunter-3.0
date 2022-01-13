import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def scrap():
    from tweet_scraper import tweet_scraper
    tweet_scraper('csgo giveaway',30,no_new_cap=5)
    tweet_scraper('csgoskins',20,no_new_cap=4)
    tweet_scraper('steam giveaway',10,no_new_cap=4)
    tweet_scraper('home',10,no_new_cap=4)
    tweet_scraper('topics',20,no_new_cap=4)

def run_app():
    from main import twittermain
    twittermain()


if __name__ == '__main__':
    clear()
    print('*****************************')
    choice = input('1. Scrape only\n2. Run app\n3. Both\n')
    if choice == '1':
        scrap()
    elif choice == '2':
        run_app()
    elif choice == '3':
        scrap()
        run_app()
    else:
        print('Invalid input')
        exit()
    print('Done')