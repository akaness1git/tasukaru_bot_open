#!/usr/bin/python3
# coding: utf-8

import os
import yaml
import modules
import logging
import datetime
import pandas as pd

book_name = "***"

class SetLogger:
    '''
    Loggerクラス
    Logのセットアップを行う。
    '''
    def __init__(self):
        self.logfh = None
        self.logger = logging.getLogger('LoggingTest')
        self.logfmt = logging.Formatter('%(asctime)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        self.log_filename = 'info.log'
        self.log_folder = './'
        self._init_log()

    def _init_log(self):
    	self.logger.setLevel(logging.INFO)
    	sh = logging.StreamHandler()
    	sh.setFormatter(self.logfmt)
    	self.logger.addHandler(sh)
    	self._refresh_log()
    
    def _refresh_log(self):
    	self.logfh = logging.FileHandler(self.log_folder+self.log_filename)
    	self.logger.addHandler(self.logfh)
    	self.logfh.setFormatter(self.logfmt)

class tasukaru:
    def __init__(self):
        self.Log = SetLogger()

    # 助かりMain
    def _tasukaru(self,url,tasukaruName):
        self.Log.logger.info("tasukaru start!")
        # 設定ファイル読み込み
        f = open("settings.yaml", "r+")
        yamldata = yaml.load(f)
        f.close()
        
        r = 0

        # Driver読み込み
        gdm = modules.GoogleDriveDriver.GoogleDriveDriver(yamldata,self.Log.logger)
        td = modules.TwitterDriver.TwitterDriver(yamldata,self.Log.logger)
        gssd = modules.GoogleSpreadSheetDriver.GoogleSpreadSheetDriver()
    
        # Twitterから各種データ読み込み
        self.Log.logger.info("Try get_twitter_images.")
        df = td.get_twitter_images(url)
        self.Log.logger.info(f"get_twitter_images is done. {len(df)} images.")
        if len(df) == 0:
            r = 9
        # ローカルに落としたいだけなら上記まででok
        links = []
        savetimes = []
        tasukarus = []
        requestTypes = []
        i = 0
        # GoogleDriveにアップロード
        for index,row in df.iterrows():
            i+=1
            self.Log.logger.info(f"[{i}/{len(df)}] Try upload.")
            filename = row['filename_tmp']
            link,savetime = gdm.upload(filename)
            links.append(link)
            savetimes.append(savetime)
            tasukarus.append(tasukaruName)
            requestTypes.append("manual")
            os.remove(filename)
            self.Log.logger.info(f"[{i}/{len(df)}] upload is done.")
        df['fileName'] = links
        df['save time'] = savetimes
        df['tasukaru'] = tasukarus
        df['requestType'] = requestTypes
    
        # GoogleSpreadSheetに書き込み
        i = 0
        for index,row in df.iterrows():
            i+=1
            self.Log.logger.info(f"[{i}/{len(df)}] Try write_data.")
            gssd.write_data(book_name,row)
            self.Log.logger.info(f"[{i}/{len(df)}] write_data is done.")
        
        self.Log.logger.info("{} Done.".format(url))
        return r
    # 出すメイン
    def _dasu(self):
        self.Log.logger.info("dasu start!")
    
        # Driver読み込み
        gssd = modules.GoogleSpreadSheetDriver.GoogleSpreadSheetDriver()
    
        name,id,url = gssd.get_rand_url(book_name)
        #print("{}\n{}\n{}".format(name,id,url))
        self.Log.logger.info("dasu is done.")
        return "{}\n{}\n{}".format(name,id,url)
    
# デバッグ用
if __name__ == "__main__":
    tasukaru = tasukaru()
    #url = "https://twitter.com/hibimeganesama/status/1121275502956650496/photo/1"
    #tasukaru(url,"Akaness#2485")
    print(tasukaru._dasu())