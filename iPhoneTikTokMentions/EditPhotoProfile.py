from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneControl.iPhoneControl import iPhone_CopyPhotoVideo

def EditPhotoProfile(d, udid):
    d.open_url('snssdk1233://user/profile/edit')
    d(name='Bio').wait(10)
    d(type='XCUIElementTypeCell').child(type='XCUIElementTypeButton').click_exists()
    if d(name='View photo').exists:
        d(name='Cancel').click()
        d.swipe(0.05, 0.5, 0.95, 0.5, 0.2)
        cprint.info(f'[{udid}] || Account avatar is exists!')
        return True

    iPhone_CopyPhotoVideo(d, udid, video_mode='Avatar')
    d(name='Upload photo').wait(5)

    timer = datetime.now()
    while not (d(name='Save').exists or d(name='Save & post').exists):
        if BadTimer(udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno) == False: return False
        try:
            if all(not d(name=n).exists for n in ['(collectionView)', 'Upload photo', 'Allow Full Access']): d(type='XCUIElementTypeCell').child(type='XCUIElementTypeButton').click_exists(); d(name='Edit photo or avatar', visible=True).click_exists()
            sleep(0.5)
            d(name='Upload photo').click_exists()
            sleep(0.5)
            d.visible_click_exists('Upload')
            sleep(0.5)
            d.alert.click_exists('Allow Full Access')
            d(name='(collectionView)').child(type='XCUIElementTypeCell').click_exists()
            if d(name='Open settings', visible=True).exists:
                d(name='Cancel', visible=True).click()
                d.open_url("App-prefs:Privacy&path=PHOTOS")
                d(name='TikTok', visible=True).click()
                d(name='Full Access', visible=True).click()
                d(name='Allow Full Access', visible=True).click()
                d.open_url('snssdk1233://user/profile/edit')
        except: pass

    d(name='Post this photo to Story').click_exists()

    for _ in range(5):
        if d(name='Save & post').exists:
            if d(name='Post this photo').exists: d(name='Post this photo').click()
            if d(name='Post this photo to Story').exists: d(name='Post this photo to Story').click()
        try:
            d(name='Save').click_exists()
            d(name='Save').wait_gone(3)
        except: pass

        if d(name='Change photo', visible=True).exists: break

    if d(name='Save').exists or d(name='Crop').exists:
        cprint.fatal(f'[{udid}] || Account banned for edit profile!')
        return False
    cprint.info(f'[{udid}] || Account avatar is changed!')
