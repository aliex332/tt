import os
import sys
from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneTikTokRegister.Login import Login
from iPhoneTikTokRegister.Register import Register
from iPhoneControl.iPhoneControl import iPhone_InstallApp, iPhone_UninstallApp
from iPhoneControl.iPhoneControl import iPhone_Shortcut



class AuthTikTok:
    def __init__(self, d, udid, country_code, settings, account_data=None, email_data=None, account_network=None, mention_action=None):
        self.d = d
        self.udid = udid
        self.country_code = country_code
        self.settings = settings
        self.account_data = account_data
        self.email_data = email_data
        self.mention_action = mention_action
        self.account_network = account_network if account_network is not None else ''
        if getattr(sys, 'frozen', False): self.local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
        else: self.local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    def AuthCheck(self):
        iPhone_UninstallApp(self.udid, 'com.zhiliaoapp.musically')
        cprint.warn(f'[{self.udid}] || START: Installing TikTok app...')
        iPhone_InstallApp(self.udid, path=f'{self.local_path}/resource/IPA/TikTok.ipa')

        cprint.info(f'[{self.udid}] || DONE: TikTok has been successfully installed!')
        self.d.app_start('com.zhiliaoapp.musically')
        sleep(2)
        if self.settings.get('Register'): cprint.warn(f'[{self.udid}] || START: Registering account!')
        if self.settings.get('Login'): cprint.warn(f'[{self.udid}] || START: Logging into account!')

        timer = datetime.now()
        while not (self.d(type='XCUIElementTypeTextField', nameMatches='Email', visible=True).exists or self.d(type='XCUIElementTypeTextField', valueContains='Email', visible=True).exists):
            try:
                self.d.app_start('com.zhiliaoapp.musically')
                if BadTimer(self.udid, timer, 120, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False

                if self.settings.get('Register') and not self.d(nameContains='have an account? Sign up', visible=True).click_exists(): sleep(1); self.d(nameContains='have an account? Sign up', visible=True).click_exists(); self.d.visible_click_exists('Email'); self.d.visible_click_exists('email'); self.d.visible_button_click_exist('red')
                if self.settings.get('Login') and not self.d(nameContains='have an account? Log in', visible=True).click_exists(): sleep(1); self.d(nameContains='have an account? Log in', visible=True).click_exists(); self.d(name='Add another account').click_exists(); self.d.visible_click_exists('Email'); self.d.visible_click_exists('email'); self.d.visible_button_click_exist('red')

                self.d(name='Profile', visible=True).click_exists()
            except: pass

        if self.settings.get('Register'):
            account_password, email_data = Register(self.d, self.udid, self.settings)
            if not account_password: return False

        if self.settings.get('Login'):
            if not Login(self.d, self.udid, self.account_data, self.email_data): return False

        timer = datetime.now()
        while not self.d(name='TTKProfileRootComponent').exists:
            try:
                self.d(name='Skip', visible=True).click_exists()
                self.d(name='Profile', visible=True).click_exists()
            except: pass
            if BadTimer(self.udid, timer, 180, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False

        timer = datetime.now()
        while not self.d(value='Edit profile', visible=True).exists:
            if BadTimer(self.udid, timer, 30, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: return False
            self.d.swipe_down()
            self.d.open_url('snssdk1233://user/profile/edit')
            self.d(value='Edit profile', visible=True).wait(5)

        nickname = self.d(nameMatches='tiktok.com/@').get().value.replace("tiktok.com/", "")

        if self.settings.get('Register'):
            cprint.ok(f'[{self.udid}] || DONE: Account registration is successful! Account nickname: {nickname}')
            with open(f"{self.local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt", "a") as accounts: accounts.write(f"{':'.join(filter(None, [self.country_code, nickname.replace('@', ''), account_password, email_data, self.account_network]))}\n")

        if self.settings.get('Login'): cprint.ok(f'[{self.udid}] || DONE: Account has been successfully logged in! Account nickname: {nickname}')

    def start(self):
        if self.AuthCheck() is False: return False
        self.d.app_stop('com.zhiliaoapp.musically')