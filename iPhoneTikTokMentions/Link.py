import os
import random
from time import sleep
from cprint import cprint

import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def DeleteLink(d, udid):
    d.open_url('snssdk1233://user/profile/edit')
    d(name='Bio').wait(10)
    d.swipe_up()
    if d(name='Add your website').exists: return True
    if d(text='Website').exists or d(name='Links').exists:
        d(name='Links').click_exists()
        d(name='Website').click_exists()
        for _ in range(10):
            if d(type='XCUIElementTypeTextField').exists: d(type='XCUIElementTypeTextField').get().clear_text()
            if d(type='XCUIElementTypeTextView').exists: d(type='XCUIElementTypeTextView').get().clear_text()
            d(name='Save').click_exists()
            d(name='Change photo', visible=True).wait(3)
            if not d(name='Save').exists: d.swipe(0.05, 0.5, 0.95, 0.5, 0.2); break

            if d(name='Save', visible=True).exists: cprint.fatal(f'[{udid}] || Slow down! Take new account!'); return False
        cprint.info(f'[{udid}] || Link on account is not exists!')
    else: cprint.fatal(f'[{udid}] || Link on account is not available!')

def ChangeLink(d, udid):
    cprint.warn(f'[{udid}] || Link on account is not exists! Start update!')
    d.open_url('snssdk1233://user/profile/edit')
    sleep(2)
    d.swipe_up()
    for _ in range(10):
        with open(f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Website/Website.txt', 'r') as f:
            url = f.readlines()
            random.shuffle(url)
        d(name='Links').click_exists()
        d(name='Website').click_exists()
        if d(name='Get started').exists: cprint.fatal(f'[{udid}] || Link on account is not available!'); return False
        split_index = random.randint(1, len(url[0]) - 1)
        url = url[0][:split_index] + ' ' + url[0][split_index:]
        if d(type='XCUIElementTypeTextField').exists: d(type='XCUIElementTypeTextField').get().clear_text()
        if d(type='XCUIElementTypeTextView').exists: d(type='XCUIElementTypeTextView').get().clear_text()
        d(type='XCUIElementTypeTextField').click_exists()
        d(type='XCUIElementTypeTextView').click_exists()
        d.send_keys(f'{url}')
        d(name='Save').click_exists()
        d(name='Change photo', visible=True).wait(5)
        if not d(name='Save').exists: d.swipe(0.05, 0.5, 0.95, 0.5, 0.2); break

    if d(name='Save', visible=True).exists:
        cprint.fatal(f'[{udid}] || Slow down! Take new account!')
        return False
    cprint.info(f'[{udid}] || Link on account is exists!')