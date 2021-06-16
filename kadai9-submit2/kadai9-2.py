import tweepy
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from datetime import  datetime
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
import json
import pandas as pd

with open('twitter.json') as f:
    twitter_keys = json.load(f)
api_key = twitter_keys['api_key']
api_key_secret = twitter_keys['api_key_secret']
access_token = twitter_keys['access_token']
access_token_secret = twitter_keys['access_token_secret']

url = 'https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-SHARP-SJ-AF50G-R-%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC-%E3%82%B0%E3%83%A9%E3%83%87%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%AC%E3%83%83%E3%83%89/dp/B08KJ85RJ5?ref_=fspcr_pl_dp_2_2272928051'

def set_driver(driver_path, headless_flg):
    options = ChromeOptions()

    if headless_flg == True:
        options.add_argument('--headless')

    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')       

    return Chrome(ChromeDriverManager().install(), options=options)

def job():
    auth = tweepy.OAuthHandler(api_key,api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    me = api.me()

    driver = set_driver("chromedriver.exe", False)
    driver.get(url)
    time.sleep(2)

    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    df = pd.read_csv('twitter.csv')

    if len(driver.find_elements_by_id('submit.add-to-cart-announce')) > 0: 
        if len(df) == 0:
            stock = driver.find_element_by_id('submit.add-to-cart-announce').text
            stocks = []
            stocks.append(stock)
            df['stocks'] = stocks
            df.to_csv('twitter.csv')
            api.update_status(f'{now}現在、在庫があります。')
        elif len(df) > 0:
            pass
    else:
        stocks = []
        df['stocks'] = stocks
        df.to_csv('twitter.csv')
        api.update_status(f'{now}現在、在庫がありません。')
    driver.quit()

def main():
    schedule.every(3).hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()



