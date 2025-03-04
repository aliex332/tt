from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer

def DisableComments(d, udid):
    cprint.warn(f'[{udid}] || STEP: Comments disable start!')
    timer = datetime.now()
    while not d(label='Settings', visible=True).exists:
        if BadTimer(udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno) == False: return False
        d(name='Profile', visible=True).click_exists()

    while not d(nameContains='Comments').exists:
        if BadTimer(udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno) == False: return False
        if d(label='Settings', visible=True).exists:
            d(label='Settings', visible=True).click()
            d(name='Create').click()
        if d(name='TTKProfileNavBarMenuComponent').exists:
            d(name='TTKProfileNavBarMenuComponent').click()
            d(name='TTKProfileMenuNavbarEndSettingsComponent').click()
        d(name='Settings and privacy', visible=True).click_exists()
        d(name='Privacy', visible=True).click_exists()

    d(nameContains='Comments').click()

    if d(nameMatches='Everyone').exists:
        d(nameMatches='Everyone').click()
        d(nameMatches='Friends').click()
        sleep(2)

    d.app_stop('com.zhiliaoapp.musically')
    d.app_start('com.zhiliaoapp.musically')
    sleep(2)
    d(name='Profile', visible=True).click_exists()

    cprint.info(f'[{udid}] || Comments disable successfully!')