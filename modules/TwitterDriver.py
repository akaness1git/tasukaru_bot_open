#!/usr/bin/python3
# coding: utf-8
import yaml
import json
import urllib
import pandas as pd
from pytz import timezone
from dateutil import parser
from requests_oauthlib import OAuth1Session

class TwitterDriver:
    def __init__ (self,yamldata,logger):
        CK = yamldata.get('CONSUMER_KEY')
        CS = yamldata.get('CONSUMER_SECRET')
        AT = yamldata.get('ACCESS_TOKEN')
        ATS = yamldata.get('ACCESS_TOKEN_SECRET')
        self.twitter = OAuth1Session(CK, CS, AT, ATS)
        self.show_url = 'https://api.twitter.com/1.1/statuses/show.json'
        self.logger = logger
    
    # Tweet IDよりツイートのjsonを取得
    def get_show_tweet(self,id):
        params = {'id':id}
        r = self.twitter.get(self.show_url,params=params)
        r = json.loads(r.text)
        return r
    
    # メディアURLとファイル名の取得、ついでに保存
    def get_media_url(self,src):
        results = []
        results = pd.DataFrame(columns=['url','thumburl','date','tweet_id','user_id','user_name','text','created at','fav','rt','screen_name','tweetUrl','filename_tmp'])
        if "video_info" in str(src):
            self.logger.info("This media is movie.")
        
        else:
            try:
                media = src["extended_entities"]["media"]
                for photo in media:
                    url = photo["media_url"]
                    filename = self.split_filename(url)
                    results.append([url,filename])
                    jst_time = parser.parse(src['created_at']).astimezone(timezone('Asia/Tokyo'))
                    result = pd.DataFrame([[url,url+':thumb',src['created_at'],src['id'],src['user']['id'],src['user']['name'],src['text'],jst_time,src['favorite_count'],src['retweet_count'],src['user']['screen_name'],photo['expanded_url'],filename]],columns=['url','thumburl','date','tweet_id','user_id','user_name','text','created at','fav','rt','screen_name','tweetUrl','filename_tmp'])
                    results = results.append(result)
                    with open(filename, 'wb') as f:
                        img = urllib.request.urlopen(url).read()
                        f.write(img)
            except Exception as x:
                self.logger.info("Tweets without media.")
                self.logger.info(x)
        return results
    
    # ファイル名を取得 URLの末尾をそのまま利用
    def split_filename(self,src):
        r = src.split('/')
        return r[-1]
    
    # URLからTweet IDを取得 5を直接指定する雑な作り
    def get_split_id(self,tweet_url):
        r = tweet_url.split('/')
        return int(r[5])
    
    # 助かりMain
    def get_twitter_images(self,tweet_url):
        id = self.get_split_id(tweet_url)
        r = self.get_show_tweet(id)
        r = self.get_media_url(r)
        return r