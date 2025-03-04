import os
import cv2
import sys
import random
import requests
import numpy as np
from time import sleep
from requests import post
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokMentions.Follow import Follow
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneTikTokMentions.Comments import SendComments
from iPhoneTikTokMentions.NickName import ChangeNickName
from iPhoneTikTokMentions.Bio import ChangeBio, DeleteBio
from iPhoneTikTokMentions.DeleteVideos import DeleteVideos
from iPhoneTikTokMentions.Link import ChangeLink, DeleteLink
from iPhoneTikTokMentions.EditPhotoProfile import EditPhotoProfile
from iPhoneTikTokMentions.BusinessAccountEnable import BusinessAccountEnable, BusinessRegister

class MentionAccount:
    def __init__(self, d, udid, country_code, settings):
        self.d = d
        self.udid = udid
        self.country_code = country_code
        self.settings = settings
        if getattr(sys, 'frozen', False): self.local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
        else: self.local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    def Exception(self):
        self.d.appium_settings({'snapshotMaxDepth': 17})
        self.d.app_stop('com.zhiliaoapp.musically')
        self.d.open_url('shortcuts://run-shortcut?name=Profile')
        self.d(name='Profile', visible=True).wait(10)

    # --------------------------------------------------------- USE IT ANYWHERE! --------------------------------------------------------------------------
    def GetAccountNickName(self):
        timer = datetime.now()
        while self.d(name='Change photo', visible=True).exists is False:
            if BadTimer(self.udid, timer, 30, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False
            self.d.open_url('snssdk1233://user/profile/edit')
            self.d(name='Change photo', visible=True).wait(5)

        self.d.swipe_down()
        nickname = self.d(nameMatches='tiktok.com/@').get().value.replace("tiktok.com/", "")
        self.Exception()
        return nickname

    def Follow(self):
        with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsSettings/Follow/Profiles.txt', 'r') as f:
            profile_urls = f.readlines()
            random.shuffle(profile_urls)
        if len(profile_urls) != 0: self.nick_account, self.name_account = Follow(self.d, self.udid, profile_urls[0])

    def DeleteBio(self):
        try: DeleteBio(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error deleting Bio!'); self.Exception()
        finally: self.Exception()

    def DeleteLink(self):
        try: DeleteLink(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error deleting Link!'); self.Exception()
        finally: self.Exception()

    def DeleteVideos(self):
        try: DeleteVideos(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error deleting Videos!'); self.Exception()
        finally: self.Exception()

    def VideoComments(self):
        try: SendComments(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error sending Comments!'); self.Exception()
        finally: self.Exception()

    def BusinessAccountEnable(self):
        try: BusinessAccountEnable(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error enable Business Account!'); self.Exception()
        finally: self.Exception()

    def BusinessAccountRegister(self):
        try: BusinessRegister(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error register Business Account!'); self.Exception()
        finally: self.Exception()

    def ChangeLink(self):
        try: ChangeLink(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error changing Link!'); self.Exception()
        finally: self.Exception()

    def ChangeBio(self):
        try: ChangeBio(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error changing Bio!'); self.Exception()
        finally: self.Exception()

    def ChangeAvatar(self):
        try: EditPhotoProfile(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error changing Avatar!'); self.Exception()
        finally: self.Exception()

    def ChangeNickName(self):
        try: ChangeNickName(self.d, self.udid)
        except: cprint.fatal(f'[{self.udid}] || Error changing NickName!'); self.Exception()
        finally: self.Exception()

    # --------------------------------------------------------- USE IT ONLY IN VIDEO SETTINGS! --------------------------------------------------------------------------

    def HashTags(self):
        with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsSettings/HashTags/HashtagsVideo.txt', 'r') as file_hashtags:
            hashtags = [line.rstrip() for line in file_hashtags if random.randint(0, 1) == 1]  # Собираем хэштеги
            random.shuffle(hashtags)  # Перемешиваем
            hashtags = ', '.join(random.sample(hashtags, min(len(hashtags), self.settings.get('video_hashtags').get('hashtag_count'))))

        try:
            self.d(type="XCUIElementTypeTextView").click_exists()
            self.d(type="XCUIElementTypeTextField").click_exists()
            self.d.send_keys(f'\n{hashtags}')
        except: pass

    def VideoDescriptionMention(self):
        with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsSettings/Description/DescriptionMention.txt', 'r', encoding='utf-8') as f:
            description_mention = f.readlines()
            random.shuffle(description_mention)
        if len(description_mention) != 0: self.nick_account, self.name_account = Follow(self.d, self.udid, description_mention[0])
        else: self.nick_account = None; self.name_account = None

    def VideoDescription(self):
        with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsSettings/Description/DescriptionVideo.txt', 'r', encoding='utf-8') as f:
            description_text = f.readlines()
            random.shuffle(description_text)
        self.d(type="XCUIElementTypeTextView").click_exists()
        self.d(type="XCUIElementTypeTextField").click_exists()
        self.d.send_keys(f'{description_text[0]} ')

        if self.nick_account is None or self.name_account is None: return True
        self.d(name='Mention friends in your post').click()
        for _ in range(5):
            sleep(1)
            if self.d(name='People').exists: self.d(name='People').click(); break
            if self.d(name='Recent').exists or self.d(name='Following').exists: break
        if self.d(name=f'{self.nick_account}').exists: self.d(name=f'{self.nick_account}').click_exists(); return True
        if self.d(name=f'{self.name_account}').exists: self.d(name=f'{self.name_account}').click_exists(); return True
        self.d(type="XCUIElementTypeTextField").get().set_text(f'{self.nick_account} {self.name_account}')
        for _ in range(25):
            if self.d(name=f'{self.nick_account}').exists: self.d(name=f'{self.nick_account}').click_exists(); return True
            if self.d(name=f'{self.name_account}').exists: self.d(name=f'{self.name_account}').click_exists(); return True
            self.d.send_keys('\b')
            sleep(1)