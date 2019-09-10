#!/usr/bin/python3
# coding: utf-8
import yaml
import os
from pytz import timezone
from dateutil import parser
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GoogleDriveDriver:
    def __init__ (self,yamldata,logger):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        self.folder_id = yamldata.get('folder_id')
        self.retry_count = 3
        self.logger = logger
    
    # mimeTypeの判別
    def get_mimeType(self,filename):
        extension = os.path.splitext(filename)[1][1:]
        if extension == 'jpg' or extension == 'jpeg':
            r = 'image/jpeg'
        elif extension == 'png':
            r = 'image/png'
        return r

    # 助かりMain
    # ドライブにアップロードする
    def upload(self,filename):
        
        for i in range(self.retry_count):
            try:
                # folder_idの指定がない場合はhomeに
                if self.folder_id is None:
                    f = self.drive.CreateFile({'title': filename
                                            , 'mimeType': self.get_mimeType(filename)})
                # folder_idの指定がある場合はそのフォルダに
                else:
                    f = self.drive.CreateFile({'title': filename
                                            , 'mimeType': self.get_mimeType(filename)
                                            , 'parents': [{'kind': 'drive#fileLink', 'id':self.folder_id}]})
                f.SetContentFile(filename)
                f.Upload()
                jst_time = parser.parse(f['createdDate']).astimezone(timezone('Asia/Tokyo'))
                return f['alternateLink'],jst_time
            except Exception as x:
                import traceback
                self.logger.info(f"[{i+1}/{self.retry_count}] upload error!\n{traceback.format_exc()}")