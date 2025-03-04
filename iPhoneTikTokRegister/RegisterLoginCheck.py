import os
import re
import email
import imaplib
import subprocess
import numpy as np
from PIL import Image
from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneTikTokCheckers.AccountsDataBase import GetAccountFromBase
from iPhoneTikTokMentions.DisableComments import DisableComments
from iPhoneTikTokMentions.EditPhotoProfile import EditPhotoProfile
from iPhoneTikTokRegister.RegisterEmailCode import RegisterEmailCode
from iPhoneControl.iPhoneControl import iPhone_InstallApp, iPhone_UninstallApp



class RegisterLoginAccountCheck:
    def __init__(self, d, udid, country_code, settings, account_data=None, account_vpn=None, mention_action=None):
        self.d = d
        self.udid = udid
        self.country_code = country_code
        self.settings = settings
        self.account_data = account_data
        self.mention_action = mention_action
        self.account_vpn = account_vpn.replace(".ovpn", "") if account_vpn is not None else 'NONE:NONE'
        self.email_service = 'Kopeechka'
        import sys
        if getattr(sys, 'frozen', False): self.local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
        else: self.local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    def RegisterCheck(self):
        cprint.warn(f'[{self.udid}] || STEP: Start register account!')

        timer = datetime.now()
        while not (self.d(type='XCUIElementTypeTextField', nameMatches='Email', visible=True).exists or self.d(type='XCUIElementTypeTextField', valueContains='Email', visible=True).exists):
            try:
                if BadTimer(self.udid, timer, 120, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False
                self.d(name='Don’t have an account? Sign up', visible=True).click_exists()
                self.d.app_start('com.zhiliaoapp.musically')
                self.d(nameMatches='Email').click_exists()
                self.d(nameMatches='email').click_exists()
                self.d(name='Profile', visible=True).click_exists()
            except: pass

        account_password, email_login, email_password = RegisterEmailCode(self.d, self.udid, self.email_service)
        if account_password == False: return False

        timer = datetime.now()
        while not self.d(name='TTKProfileRootComponent').exists:
            try:
                self.d(name='Skip', visible=True).click_exists()
                self.d.open_url('shortcuts://run-shortcut?name=Profile')
                sleep(1)
                # self.d(name='Profile', visible=True).click_exists()
            except: pass
            if BadTimer(self.udid, timer, 180, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False

        self.d.open_url('snssdk1233://user/profile/edit')
        self.d(name='Change photo', visible=True).wait(5)
        self.d.swipe_down()
        nickname = self.d(nameMatches='tiktok.com/@').get().value.replace("tiktok.com/", "")

        if self.settings.get('avatar_change').get('enabled'): self.mention_action.ChangeAvatar()
        cprint.warn(f'[{self.udid}] || Account register is successfully!')
        cprint.info(f'[{self.udid}] || Account nickname: {nickname}')
        with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt', 'a') as accounts: accounts.write(f'{self.udid}:{self.country_code}:{nickname.replace("@", "")}:{account_password}:{email_login}:{email_password}:{self.account_vpn}' + '\n')
        if self.settings.get('business_enable').get('enabled'): self.mention_action.BusinessAccountEnable()
        if self.settings.get('business_register').get('enabled'): self.mention_action.BusinessAccountRegister()
        return nickname

    def LoginCheck(self):
        cprint.warn(f'[{self.udid}] || STEP: Start login account!')
        account_nick, account_pass, account_vpn, country_code, account_email, account_email_pass = GetAccountFromBase(self.udid, self.account_data)

        timer = datetime.now()
        while not (self.d(type='XCUIElementTypeTextField', nameMatches='Email').exists or self.d(type='XCUIElementTypeTextField', valueContains='Email').exists):
            try:
                if BadTimer(self.udid, timer, 120, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False
                self.d.app_start('com.zhiliaoapp.musically')
                self.d(name='Already have an account? Log in', visible=True).click_exists()
                self.d(nameMatches='Email').click_exists()
                self.d(nameMatches='email').click_exists()
                self.d(name='Profile', visible=True).click_exists()
                if self.d(name='Log in to TikTok').exists: self.d.visible_button_click_exist('red')
            except: pass

        self.d(nameMatches='Email').click_exists()
        self.d.send_keys(account_nick)
        if self.d(name='Password', visible=True).exists or self.d(value='Password', visible=True).exists: pass
        else: self.d(name='Continue', visible=True).click()

        self.d(name='Password', visible=True).click_exists()
        self.d(value='Password', visible=True).click_exists()
        self.d.send_keys(account_pass)

        timer = datetime.now()
        max_numbs = 0
        while not (self.d(name='Skip', visible=True).exists or self.d(name='Profile', visible=True).exists):
            if BadTimer(self.udid, timer, 250, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False
            self.d.visible_button_click_exist('red')
            if self.d(name='Your account was permanently banned').exists or self.d(name='Your account was permanently banned due to multiple violations of our Community Gudelines.').exists or self.d(name='Log out').exists or self.d(name='Download your data').exists or self.d(name='Account is currently suspended').exists:
                cprint.fatal(f'[{self.udid}] || Account permanently banned! Take new account!')

                with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt', 'r') as file: lines = file.readlines()
                updated_lines = [line for line in lines if self.account_data not in line]
                with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt', 'w') as file: file.writelines(updated_lines)
                with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsDataBase/BannedAccounts.txt', 'a') as banned_file: banned_file.write(f'{self.account_data}\n')
                raise ValueError

            if self.d(name='Maximum number of attempts reached. Try again later.').exists:
                cprint.fatal(f'[{self.udid}] || Maximum number of attemps reached! Try set VPN! Take new account!')
                if max_numbs == 2: return False
                max_numbs += 1
            if self.d(name='Verify identity', visible=True).exists:
                cprint.fatal(f'[{self.udid}] || Verify your account by Email!')
                self.d(nameContains='Email').click()
                sleep(1)
                try: self.d(name='Next', visible=True).click()
                except: pass
                self.d(name='Enter 6-digit code').wait(15)
                sleep(10)
                mail = imaplib.IMAP4_SSL('imap.firstmail.ltd', 993)
                mail.login(account_email, account_email_pass)
                mail.select('INBOX')
                _, data = mail.search(None, '(FROM "register@account.tiktok.com")')
                _, data = mail.fetch(data[0].split()[-1], "(RFC822)")
                code = re.findall(r'\d+', email.message_from_bytes(data[0][1]).get('Subject'))
                cprint.info(f'[{self.udid}] || TikTok verify code: {code[0]}!')
                self.d.send_keys(code)
                sleep(10)


        timer = datetime.now()
        while not self.d(name='TTKProfileRootComponent').exists:
            if BadTimer(self.udid, timer, 250, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False
            try:
                # self.d.open_url('shortcuts://run-shortcut?name=Profile')
                sleep(1)
                self.d(name='Profile', visible=True).click_exists()
            except: pass

        timer = datetime.now()
        while not self.d(name='Change photo', visible=True).exists:
            if BadTimer(self.udid, timer, 30, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False
            self.d.open_url('snssdk1233://user/profile/edit')
            self.d(name='Change photo', visible=True).wait(5)

        self.d.swipe_down()
        nickname = self.d(nameMatches='tiktok.com/@').get().value.replace("tiktok.com/", "")

        if self.settings.get('avatar_change').get('enabled'): self.mention_action.ChangeAvatar()
        cprint.info(f'[{self.udid}] || Account logined is successfully!')
        cprint.info(f'[{self.udid}] || Account nickname: {nickname}')
        if self.settings.get('business_enable').get('enabled'): self.mention_action.BusinessAccountEnable()
        if self.settings.get('business_register').get('enabled'): self.mention_action.BusinessAccountRegister()
        return nickname


    def CheckInstallTikTok(self):
        iPhone_UninstallApp(self.udid, 'com.zhiliaoapp.musically')
        cprint.warn(f'[{self.udid}] || TikTok is not installed! Start install!')
        print(f'{self.local_path}/resource/IPA/TikTok.ipa')
        iPhone_InstallApp(self.udid, path=f'{self.local_path}/resource/IPA/TikTok.ipa')

        cprint.info(f'[{self.udid}] || TikTok is successfully installed!')
        retries = 0
        while retries < 5:
            try: self.d.app_stop('com.zhiliaoapp.musically'); self.d.app_start('com.zhiliaoapp.musically'); return True
            except: retries += 1; sleep(5)
        return False

    def start(self):
        self.CheckInstallTikTok()
        if self.settings.get('Register') and (nickname := self.RegisterCheck()) is False: return False
        if self.settings.get('Login') and (nickname := self.LoginCheck()) is False: return False
        self.d.app_stop('com.zhiliaoapp.musically')
        return nickname