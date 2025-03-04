import os
import re
import random
from time import sleep
from icecream import ic
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneTikTokMentions.MentionAccount import MentionAccount
from iPhoneControl.iPhoneControl import iPhone_CopyPhotoVideo

class VideoUploaderTikTok:
    def __init__(self, d, udid, country_code, settings, mention_action=None):
        self.udid = udid
        self.d = d
        self.country_code = country_code
        self.settings = settings
        self.mention_action = mention_action
        self.d.appium_settings({'snapshotMaxDepth': 17})

        if self.settings.get('use_again_switch').get('enabled'): self.laps_for_upload = self.settings.get('use_again_switch').get('lap_count'); self.sleep_for_laps = (self.settings.get('use_again_switch').get('sleep_count')) * 60
        else: self.laps_for_upload = 1; self.sleep_for_laps = 0
        self.video_upload_count = self.settings.get('videos_count')

        import sys
        if getattr(sys, 'frozen', False): self.local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
        else: self.local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    def Exception(self):
        self.d.appium_settings({'snapshotMaxDepth': 17})
        self.d.app_stop('com.zhiliaoapp.musically')
        self.d.open_url('shortcuts://run-shortcut?name=Profile')
        self.d(name='Profile', visible=True).wait(10)

    def ProfileButton(self):
        timer = datetime.now()
        self.d.appium_settings({'snapshotMaxDepth': 17})
        while not self.d(name='TTKProfileRootComponent').exists:
            if BadTimer(self.udid, timer, 30, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) == False: self.Exception(); break
            self.d(name='Profile', visible=True).click_exists()

    def RecordButton(self):
        timer = datetime.now()
        while self.d(name='recordPageUploadButton', visible=True).exists is False:
            if BadTimer(self.udid, timer, 40, extract_stack()[-1].name, extract_stack()[-1].lineno) is False: return False
            self.d.open_url('shortcuts://run-shortcut?name=Profile')
            self.d.open_url('shortcuts://run-shortcut?name=Record')
            self.d(name='recordPageUploadButton', visible=True).wait(5)
            if self.d(name='recordPageUploadButton', visible=True).exists: break
            self.d(name='Continue').click_exists()
            self.d.alert.click_exists('Cancel')
            self.d.alert.click_exists('Allow')
            self.d.alert.click_exists('Allow Full Access')

    def CopyPhotoVideo(self):
        if self.settings.get('Video'): iPhone_CopyPhotoVideo(self.d, self.udid, video_mode='Video')
        if self.settings.get('Photo'): iPhone_CopyPhotoVideo(self.d, self.udid, video_mode='Photo', photo_count=self.settings.get('photo_count'))
        if self.settings.get('Autocut'): iPhone_CopyPhotoVideo(self.d, self.udid, video_mode='Autocut', photo_count=self.settings.get('photo_count'))
        if self.settings.get('Overlay'): iPhone_CopyPhotoVideo(self.d, self.udid, video_mode='Overlay')

    def MusicOpen(self):
        if self.settings.get('use_music_switch') is False:
            if self.RecordButton() is False: return False
            return True

        if os.path.isfile(f'{self.local_path}/iPhoneTikTokFiles/AccountsSettings/Music/Music{self.country_code}.txt') is False:
            cprint.info(f'[{self.udid}] || Music file: Music{self.country_code} not found! Start upload without sound!')
            if self.RecordButton() is False: return False
            return True

        with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsSettings/Music/Music{self.country_code}.txt', 'r') as f:
            music_urls = f.readlines()
            random.shuffle(music_urls)

        if not music_urls:
            cprint.info(f'[{self.udid}] || Music file: Music{self.country_code} is empty! Start upload without sound!')
            if self.RecordButton() is False: return False
            return True

        self.d.open_url(f'{music_urls[0]}')
        cprint.info(f'[{self.udid}] || Music is open.')
        timer = datetime.now()
        bad_music = 0
        while not self.d(name='recorderPageToolBarSwapCamera', visible=True).exists:
            if self.d(name="This sound isn't available.", visible=True).exists or self.d(name="This sound isn’t available.", visible=True).exists or bad_music == 10 or BadTimer(self.udid, timer, 40, extract_stack()[-1].name, extract_stack()[-1].lineno) is False:
                cprint.fatal(f'[{self.udid}] || This sound is not available. Sound deleted!')
                new_music = re.compile(re.escape(music_urls.pop(0).strip()))
                with open(f'{self.local_path}/iPhoneTikTokFiles/AccountsSettings/Music/Music{self.country_code}.txt', 'w') as f: f.writelines(line for line in music_urls if not new_music.fullmatch(line.strip()))
                self.Exception()
                return False
            self.d(name='Use this sound').click_exists()
            self.d(name='Use sound').click_exists()
            sleep(1)
            bad_music += 1

    def UploadButton(self):
        sleep(2)
        self.d.appium_settings({'snapshotMaxDepth': 17})

        timer = datetime.now()
        while self.d(name='Record video').exists is False:
            if BadTimer(self.udid, timer, 40, extract_stack()[-1].name, extract_stack()[-1].lineno) is False: return False
            self.d(name='Continue').click_exists()
            self.d.alert.click_exists('Allow')
            self.d.alert.click_exists('Allow Full Access')
            self.d(name='Create a video of up to 15 seconds').click_exists()
            self.d(name='Create a video of up to 60 seconds').click_exists()


        if self.settings.get('Overlay'):
            with open(f'{self.local_path}/iPhoneTikTokFiles/Overlay/OverlaySettings.txt', 'r') as f:
                overlay_urls = f.readlines()
                random.shuffle(overlay_urls)

            if overlay_urls and overlay_urls[0].strip():
                self.d.open_url(f'{overlay_urls[0]}')
                timer = datetime.now()
                while not self.d(name='Next').exists:
                    if BadTimer(self.udid, timer, 120, extract_stack()[-1].name, extract_stack()[-1].lineno) is False: return False
                    self.d(name='Use this effect').click_exists()
                    self.d(name='(recordPageEffectsEntrance)').click_exists()
                    self.d(name='CAK_cell_id_ACCAssetThumbViewModel').click_exists()
                self.d(name='Next').click()
            else:  cprint.fatal(f'[{self.udid}] || Your overlay settings is empty! We can use record mode only!')
            self.d(label='Front-facing camera view on. Flip camera view').click_exists()
            self.d(name='Create a video of up to 60 seconds').click()
            self.d(name='Record video').click()
            sleep(self.settings.get('record_time') + 0.5)
            self.d(name='(recordPageCompleteButton)').click()

        if self.settings.get('Record'):
            self.d(label='Front-facing camera view on. Flip camera view').click_exists()
            self.d(name='Create a video of up to 60 seconds').click()
            self.d(name='Record video').click()
            sleep(self.settings.get('record_time') + 0.5)
            self.d(name='(recordPageCompleteButton)').click()

        if self.settings.get('Photo') or self.settings.get('Video') or self.settings.get('Autocut'):
            timer = datetime.now()
            while self.d(name='Select', visible=True).exists is False:
                if BadTimer(self.udid, timer, 40, extract_stack()[-1].name, extract_stack()[-1].lineno) is False: return False
                self.d(name='recordPageUploadButton').click_exists()
                self.d.alert.click_exists('Allow Full Access')
                if self.settings.get('Video'): self.d(value='Videos').click_exists()
                if self.settings.get('Photo'): self.d(value='Photos').click_exists()
                if self.d(name='Next').exists is False: self.d(name='Select multiple').click_exists()
                self.d(name='(collectionView)').child(type='XCUIElementTypeCell').click_exists()

        if self.settings.get('Photo') or self.settings.get('Autocut'):
            timer = datetime.now()
            while self.d(name='This is the last item', visible=True).exists is False:
                if BadTimer(self.udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno, self.d) is False: return False
                self.d(name='Select').click_exists()
                self.d.swipe_left()
            if self.settings.get('Autocut'): self.d(text='AutoCut').click()

        timer = datetime.now()
        while not self.d(name='Drafts').exists:
            if BadTimer(self.udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno) is False: return False
            self.d(nameContains='Next').click_exists()
            sleep(0.5)

        try:
            if self.d(type='XCUIElementTypeTextField').exists: self.d(type='XCUIElementTypeTextField').get().clear_text()
            if self.d(type='XCUIElementTypeTextView').exists: self.d(type='XCUIElementTypeTextView').get().clear_text()
        except:
            if self.d(type='XCUIElementTypeTextField').exists: self.d(type='XCUIElementTypeTextField').get().clear_text()
            if self.d(type='XCUIElementTypeTextView').exists: self.d(type='XCUIElementTypeTextView').get().clear_text()
        finally: pass

    def PostVideo(self):
        if self.settings.get('video_description').get('enabled'): self.mention_action.VideoDescription()
        if self.settings.get('video_hashtags').get('enabled'): self.mention_action.HashTags()

        self.d(value='Preview').click_exists()
        self.d(value='Cover').click_exists()
        self.d(value='Post').click()
        self.d(value='Post video', visible=True).click_exists()
        self.d(value='Post Now', visible=True).click_exists()
        self.d(name='Confirm').click_exists()
        self.d.appium_settings({'snapshotMaxDepth': 15})

        for _ in range(20):
            if self.d(nameContains='Video posted!').exists: sleep(2); break
            if self.d.alert.exists:
                self.d.alert.click_exists('OK')
                self.d.alert.click_exists('Allow')
                self.d.alert.click_exists('Cancel')
                self.d.alert.click_exists('Allow Full Access')
                self.d.alert.click_exists('Ask App Not to Track')
            sleep(0.5)
        self.d.app_stop('com.zhiliaoapp.musically')

    def CheckBan(self):
        if self.d(name='Your account was logged out. Try logging in again.', visible=True).exists: cprint.fatal(f'[{self.udid}] || Account banned! Take new account!'); return False
        if self.d(name='Account status', visible=True).exists: cprint.fatal(f'[{self.udid}] || Account banned! Take new account!'); return False

    def start(self):
        self.d.app_start('com.zhiliaoapp.musically')
        if self.settings.get('link_change').get('enabled'): self.mention_action.BusinessAccountEnable()
        if self.settings.get('nickname_change').get('enabled') and self.settings.get('nickname_change').get('when') == 'Before': self.mention_action.ChangeNickName()
        if self.settings.get('link_change').get('enabled') and self.settings.get('link_change').get('when') == 'Before': self.mention_action.ChangeLink()
        if self.settings.get('bio_change').get('enabled') and self.settings.get('bio_change').get('when') == 'Before': self.mention_action.ChangeBio()

        for lap in range(self.laps_for_upload):
            if self.settings.get('delete_bio').get('enabled'): self.mention_action.DeleteBio()
            if self.settings.get('delete_link').get('enabled'): self.mention_action.DeleteLink()
            if self.settings.get('delete_video').get('enabled'): self.mention_action.DeleteVideos()
            if self.settings.get('video_description').get('enabled'): self.mention_action.VideoDescriptionMention()

            success_upload = 0
            cprint.warn(f'[{self.udid}] || STEP: Start video upload. Current lap: {lap} | Laps for upload: {self.laps_for_upload} | Sleep time: {self.sleep_for_laps} | One lap include: {self.video_upload_count} video.')
            self.CopyPhotoVideo()
            timer = datetime.now()
            while not success_upload == self.video_upload_count:
                if BadTimer(self.udid, timer, 600, extract_stack()[-1].name, extract_stack()[-1].lineno) is False: return False
                try:
                    if self.CheckBan() is False: return False
                    if self.MusicOpen() is False: self.Exception(); continue
                    if self.UploadButton() is False: self.Exception(); continue
                    if self.PostVideo() is False: self.Exception(); continue
                except:
                    cprint.fatal(f'[{self.udid}] || Error with video upload!')
                    self.Exception()
                    self.ProfileButton()
                    continue
                finally: pass

                success_upload += 1
                cprint.info(f'[{self.udid}] || Video upload! Count: {success_upload}.')
                if success_upload != self.video_upload_count: self.CopyPhotoVideo()

            if self.settings.get('nickname_change').get('enabled') and self.settings.get('nickname_change').get('when') == 'After': self.mention_action.ChangeNickName()
            if self.settings.get('link_change').get('enabled') and self.settings.get('link_change').get('when') == 'After': self.mention_action.ChangeLink()
            if self.settings.get('bio_change').get('enabled') and self.settings.get('bio_change').get('when') == 'After': self.mention_action.ChangeBio()
            if self.settings.get('send_comments').get('enabled'): self.mention_action.VideoComments()

            sleep(self.sleep_for_laps)

        return False