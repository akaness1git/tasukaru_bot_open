#!/usr/bin/python3
# coding: utf-8

import gspread
import pandas as pd
import random
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSpreadSheetDriver:
    def __init__ (self):
        self.scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('imageuploader-d6459e1511cf.json', self.scope)
        self.gc = gspread.authorize(self.credentials)
    
    # ワークブックを開く
    def open_workbook(self,bookname):
        self.wb = self.gc.open(bookname)
    
    # ワークシートを開く
    # 指定がない場合は1枚目
    def open_worksheet(self,sheetname=0):
        self.ws = self.wb.get_worksheet(sheetname)
    
    # 列のデータを取得 未使用
    # 指定がない場合はA列
    def get_colmuns(self,col_index=1):
        values_list = self.ws.col_values(col_index)
        return values_list
    
    # 最終行番号取得
    def get_lastrow(self):
        return len(self.get_colmuns())

    # 助かりMain
    def write_data(self,bookname,data):
        self.open_workbook(bookname)
        self.open_worksheet()
    
        self.ws.append_row([str(data['url'])
                            , str(data['thumburl'])
                            , str(data['date'])
                            , str(data['tweet_id'])
                            , str(data['user_id'])
                            , str(data['user_name'])
                            , str(data['text'])
                            , str(data['created at'])
                            , str(data['save time'])
                            , str(data['requestType'])
                            , str(data['fav'])
                            , str(data['rt'])
                            , str(data['screen_name'])
                            , str(data['tweetUrl'])
                            , str(data['fileName'])
                            , str(data['tasukaru'])
                            ])
    # 出すメイン
    def get_rand_url(self,bookname):
        self.open_workbook(bookname)
        self.open_worksheet()
        rows = self.get_lastrow()
        row = random.randint(2,int(rows))
        name = str(self.ws.acell('F'+str(row)).value)
        id = "@" + str(self.ws.acell('M'+str(row)).value)
        url = str(self.ws.acell('N'+str(row)).value)
        return name,id,url

    
    # 行追加はせずに最終行に追記したい場合はこっち 未使用
    def write_data_lastrow(self,bookname,data):
        self.open_workbook(bookname)
        self.open_worksheet()

        last_row = self.get_lastrow()
        
        self.ws.update_acell('A'+str(last_row), str(data['url']))
        self.ws.update_acell('B'+str(last_row), str(data['thumburl']))
        self.ws.update_acell('C'+str(last_row), str(data['date']))
        self.ws.update_acell('D'+str(last_row), str(data['tweet_id']))
        self.ws.update_acell('E'+str(last_row), str(data['user_id']))
        self.ws.update_acell('F'+str(last_row), str(data['user_name']))
        self.ws.update_acell('G'+str(last_row), str(data['text']))
        self.ws.update_acell('H'+str(last_row), str(data['created at']))
        self.ws.update_acell('I'+str(last_row), str(data['save time']))
        self.ws.update_acell('J'+str(last_row), str(data['requestType']))
        self.ws.update_acell('K'+str(last_row), str(data['fav']))
        self.ws.update_acell('L'+str(last_row), str(data['rt']))
        self.ws.update_acell('M'+str(last_row), str(data['screen_name']))
        self.ws.update_acell('N'+str(last_row), str(data['tweetUrl']))
        self.ws.update_acell('O'+str(last_row), str(data['fileName']))
        self.ws.update_acell('P'+str(last_row), str(data['tasukaru']))