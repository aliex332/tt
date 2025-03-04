import os
import random
from time import sleep
from cprint import cprint

import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')


def Follow(d, udid, profile):
    d.open_url(f'{profile}')
    sleep(2)
    d.appium_settings({'snapshotMaxDepth': 20})
    for _ in range(20):
        sleep(0.5)
        d(text='Follow').click_exists()
        if d(labelContains='@').exists:
            if d(name='TTKProfileInfoBaseInfoItemComponent').exists:
                nick_account = d(name='TTKProfileInfoBaseInfoItemComponent').get().text
                if d(textMatches='Profile photo').exists: name_account = d(textMatches='Profile photo').get().text; name_account = name_account.replace(", Profile photo,", "")
            break
    d.swipe(0.1, 0.5, 0.9, 0.5, 0.1)
    sleep(2)
    cprint.info(f'[{udid}] || Follow for mention! Name: {name_account}. Nick: {nick_account}')
    d.appium_settings({'snapshotMaxDepth': 17})
    d.swipe(0.1, 0.5, 0.9, 0.5, 0.1)
    return nick_account, name_account