import os
import random
from time import sleep
from cprint import cprint
from iPhoneTikTokMentions.Follow import Follow

import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')


def DeleteBio(d, udid):
    d.open_url('snssdk1233://user/profile/edit')
    d(name='Bio').wait(10)
    sleep(2)
    if d(name='Add a bio').exists: cprint.info(f'[{udid}] || Bio deleted!'); return True
    d(name='Bio').click()
    for _ in range(10):
        if d(name='Save').exists:
            sleep(0.5)
            if d(type='XCUIElementTypeTextField').exists: d(type='XCUIElementTypeTextField').get().clear_text()
            if d(type='XCUIElementTypeTextView').exists: d(type='XCUIElementTypeTextView').get().clear_text()
            d(name='Save').click_exists()
            d(name='Change photo', visible=True).wait(3)
            if d(name='Change photo', visible=True).exists: d.swipe(0.05, 0.5, 0.95, 0.5, 0.2); break
    cprint.info(f'[{udid}] || Bio deleted!')
        
def ChangeBio(d, udid):
    with open(f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Bio/BioMention.txt', 'r') as f:
        profile_urls = f.readlines()
        random.shuffle(profile_urls)
    if len(profile_urls) != 0: nick_account, name_account = Follow(d, udid, profile_urls[0])

    cprint.warn(f'[{udid}] || Bio on account is not exists! Start update!')
    d.open_url('snssdk1233://user/profile/edit')
    d(name='Bio').wait(5)
    d(name='Bio').click()
    for _ in range(10):
        if d(type='XCUIElementTypeTextField').exists: d(type='XCUIElementTypeTextField').get().clear_text()
        if d(type='XCUIElementTypeTextView').exists: d(type='XCUIElementTypeTextView').get().clear_text()
        with open(f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Bio/BioText.txt', 'r', encoding='utf-8') as f:
            name_text = f.readlines()
            name_text = [line.strip() for line in name_text]
            random.shuffle(name_text)

        if len(profile_urls) != 0:
            d.send_keys(f'{name_text[0]}\n{nick_account}')
            d(name=name_account).wait(10)
            sleep(2)
            d(name=name_account).click_exists()

        if len(profile_urls) == 0:
            d.send_keys(f'{name_text[0]}')

        d(name='Save').click_exists()
        d(name='Change photo', visible=True).wait(5)
        if d(name='Change photo', visible=True).exists: d.swipe(0.05, 0.5, 0.95, 0.5, 0.2); break

    if d(name='Save', visible=True).exists: cprint.fatal(f'[{udid}] || Slow down! Take new account!'); return False
    cprint.info(f'[{udid}] || Bio changed!')