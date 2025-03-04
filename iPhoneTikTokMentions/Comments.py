import os
import random
from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneTikTokMentions.Follow import Follow
import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def DisableComments(d, udid):
    d.app_stop('com.zhiliaoapp.musically')
    sleep(1)
    d.open_url('snssdk1233://setting')
    timer = datetime.now()
    while d(nameContains='Comments').exists is False:
        if BadTimer(udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno) is False: return False
        d(name='Privacy', visible=True).click_exists()

    d(nameContains='Comments').click()
    if d(nameContains='Everyone').exists: d(nameContains='Everyone').click(); d.visible_wait('Friends', 10); d.visible_click('Friends')
    if d(nameContains='Friends').exists: pass
    cprint.info(f'[{udid}] || Comments disable successfully!')

def SendComments(d, udid):
    DisableComments(d, udid)
    with open(f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Comments/CommentsMention.txt', 'r', encoding='utf-8') as f:
        comments_mention = f.readlines()
        comments_mention = [line.strip() for line in comments_mention]
        random.shuffle(comments_mention)

    if len(comments_mention) != 0: nick_account, name_account = Follow(d, udid, comments_mention[0])
    
    d.open_url('snssdk1233://webview?url=https://inapp.tiktokv.com/tpp/inapp/pns_product_poseidon/video_permission_batch_management.html')
    d(name='All').wait(10)
    
    cprint.warn(f'[{udid}] || Start write comments on videos!')
    sleep(5)
    d.appium_settings({'snapshotMaxDepth': 17})
    if d(value='No posts yet', visible=True).exists: cprint.fatal(f'[{udid}] || Videos for comments not exists!'); return True
    if d.xpath('//XCUIElementTypeStaticText[@value="Today"]').exists: video_count = d.xpath('//XCUIElementTypeStaticText[@value="Today"]').find_elements()
    if d.xpath('//XCUIElementTypeStaticText[@value="Yesterday"]').exists: video_count = d.xpath('//XCUIElementTypeStaticText[@value="Yesterday"]').find_elements()
    for _ in range(len(video_count)):
        if d(value='All').exists:
            x = d(value='All').get().bounds.x
            if _ == 5: d.swipe_up(); sleep(0.5)
            y = video_count[_].bounds.y
            d.click(x, y)
            d(name='feedCommentButton').wait(3)
            if d(name='feedCommentButton').exists:
                while d(value='Manage post visibility', visible=True).exists is False:
                    try:
                        d(name='feedCommentButton', visible=True).click_exists()
                        with open(f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Comments/CommentsText.txt', 'r', encoding='utf-8') as f:
                            comments_text = f.readlines()
                            comments_text = [line.strip() for line in comments_text]
                            random.shuffle(comments_text)
                        if d(name='Send').exists:
                            d.appium_settings({'snapshotMaxDepth': 20, 'maxTypingFrequency': 20})
                            if nick_account:
                                if d(type='XCUIElementTypeTextField').exists: d(type='XCUIElementTypeTextField').get().set_text(f'{comments_text[0]} ')
                                if d(type='XCUIElementTypeTextView').exists: d(type='XCUIElementTypeTextView').get().set_text(f'{comments_text[0]} ')
                                d.appium_settings({'snapshotMaxDepth': 20, 'maxTypingFrequency': 1})
                                d.send_keys('@')
                                d(name=name_account).wait(2)
                                if d(name=name_account).exists: d(name=name_account).click()
                                else:
                                    d.send_keys('\b')
                                    d.send_keys(nick_account)
                                    for _ in range(10):
                                        d(name=name_account).wait(2)
                                        sleep(0.5)
                                        if d(name=name_account).exists: d(name=name_account).click(); break
                                        d.send_keys('\b')
                            else:
                                if d(type='XCUIElementTypeTextField').exists: d(type='XCUIElementTypeTextField').get().set_text(f'{comments_text[0]} ')
                                if d(type='XCUIElementTypeTextView').exists: d(type='XCUIElementTypeTextView').get().set_text(f'{comments_text[0]} ')

                            # d(value='not selected').click()
                            d.send_keys('\n')
                            d.appium_settings({'snapshotMaxDepth': 17, 'maxTypingFrequency': 17})
                        d(name='Close comment section', visible=True).click_exists()
                        sleep(0.5)
                        d(name='returnButton', visible=True).click_exists()
                    except: pass
                d(name='All').wait(10)
        cprint.info(f'[{udid}] || Comment send! Video: {_ + 1}')