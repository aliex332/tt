import random
import wda
from time import time
from time import sleep
from cprint import cprint
from iPhoneNetSecurity.OpenVPNConnect import ConnectVPN
from iPhoneTikTokCheckers.WatcherFunction import Alert_Watcher
from iPhoneTikTokMentions.MentionAccount import MentionAccount
from iPhoneTikTokCheckers.AccountsDataBase import GetAccountFromBase
from iPhoneTikTokUpload.VideoUploader import VideoUploaderTikTok
from iPhoneTikTokRegister.RegisterLoginCheck import RegisterLoginAccountCheck
from iPhoneControl.iPhoneControl import iPhone_ConnectPC, iPhone_SetRegion, iPhoneNetworkReset


class iPhoneTikTok:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'disable_pop_up') and self.disable_pop_up is not None:
            self.disable_pop_up.stop()

        end_time = time()
        elapsed_time = end_time - self.start_time

        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        cprint.ok(f'[{self.udid}] || Used time for this: {minutes} min {seconds} sec.')
        sleep(0.5)

    def __init__(self, udid,
                 settings,
                 country_code=None,
                 account_data=None):

        self.settings = settings
        if self.settings.get('Login') and not GetAccountFromBase(udid, account_data): raise ValueError
        self.start_time = time()
        # if hard_reset is not False: iPhoneHardReset(udid)
        if self.settings.get('reset_network'): iPhoneNetworkReset(udid)
        self.udid = udid
        self.country_code = country_code
        if iPhone_ConnectPC(udid) is False: raise RuntimeError("Device is offline")
        if self.settings.get('Register') or self.settings.get('Upload') or self.settings.get('Mention'): self.account_nick = None; self.account_vpn = None

        # LOGIN
        self.account_data = account_data
        if self.settings.get('Login'): (self.account_nick,
                              self.account_pass,
                              self.account_vpn,
                              self.country_code,
                              self.account_email,
                              self.account_email_pass) = (GetAccountFromBase(udid, account_data)); cprint.warn(f'[{udid}] || STEP: Login to account: @{self.account_nick} | COUNTRY: {self.country_code} | VPN: {self.account_vpn}')

        self.d = wda.USBClient(self.udid)
        self.d.appium_settings({'snapshotMaxDepth': 17, 'maxTypingFrequency': 20})
        self.disable_pop_up = Alert_Watcher(self.d, self.udid)
        self.disable_pop_up.start()
        self.mention_action = MentionAccount(self.d, self.udid, self.country_code, self.settings) if self.settings.get('Mention') else None
        if self.settings.get('Register') or self.settings.get('Login'): iPhone_SetRegion(self.udid, self.country_code)
        if self.settings.get('vpn_enable') or self.account_vpn: self.account_vpn = ConnectVPN(self.d, self.udid, self.country_code, self.account_vpn)
    def RegisterLoginAccount(self):
        self.register_login = RegisterLoginAccountCheck(self.d,
                                                        self.udid,
                                                        country_code=self.country_code,
                                                        account_data=self.account_data,
                                                        account_vpn=self.account_vpn,
                                                        settings=self.settings,
                                                        mention_action=self.mention_action)

        if self.register_login.start() is False: return False

    def UploadVideo(self):
        self.upload_video = VideoUploaderTikTok(self.d,
                                                self.udid,
                                                settings=self.settings,
                                                country_code=self.country_code,
                                                mention_action=self.mention_action)

        if self.upload_video.start() is False: return False

    def Mention(self):
        if self.settings.get('delete_bio').get('enabled'): self.mention_action.DeleteBio()
        if self.settings.get('delete_link').get('enabled'): self.mention_action.DeleteLink()
        if self.settings.get('delete_video').get('enabled'): self.mention_action.DeleteVideos()
        if self.settings.get('follow_account').get('enabled'): self.mention_action.Follow()
        if self.settings.get('send_comments').get('enabled'): self.mention_action.VideoComments()
        if self.settings.get('link_change').get('enabled'): self.mention_action.ChangeLink()
        if self.settings.get('bio_change').get('enabled'): self.mention_action.ChangeBio()
        if self.settings.get('nickname_change').get('enabled'): self.mention_action.ChangeNickName()
        if self.settings.get('avatar_change').get('enabled'): self.mention_action.ChangeAvatar()
        if self.settings.get('business_enable').get('enabled'): self.mention_action.BusinessAccountEnable()
        if self.settings.get('business_register').get('enabled'): self.mention_action.BusinessAccountRegister()