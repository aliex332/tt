import os
import random
from time import sleep
from cprint import cprint
import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')


def DeleteVideos(d, udid):
    d.open_url('snssdk1233://webview?url=https://inapp.tiktokv.com/tpp/inapp/pns_product_poseidon/video_permission_batch_management.html')
    for _ in range(10):
        if d(value="No posts yet", visible=True).exists: cprint.info(f'[{udid}] || Videos on account is not exists!'); Exception(); return True
        if d(name='All').exists: break
        sleep(0.5)

    cprint.warn(f'[{udid}] || Videos on account is exists! Start delete!')
    while d(value='Everyone', name='Everyone').count() != 1:
        d(nameContains='Manage post', visible=True).click_exists()
        if d(value='No posts yet', visible=True).exists: break
        if d(value='All').exists:
            x = d(value='All').get().bounds.x
            y = d(value='Everyone', name='Everyone')[1].get().bounds.y
            d.click(x, y)

        d(name='feedShareButton').wait(3)
        if d(name='feedShareButton').exists:
            while d(value='Manage post visibility', visible=True).exists is False:
                d(name='Close').click_exists()
                d(name='feedShareButton').click_exists()
                x, y = d(nameContains='Save').get().bounds.center
                for _ in range(4): d.swipe(x, y, x - 50, y, duration=0.1)

                if d(name='Delete', visible=True).exists:
                    d(name='Delete', visible=True).click_exists()
                    sleep(2)
                    d(value='Delete').click_exists()
                    sleep(2)

                if d(name='Close').exists:
                    x = d(name='Close').get().bounds.x
                    d.click(x, y)
                    sleep(2)
                    d(value='Delete').click_exists()
                    sleep(2)

    cprint.info(f'[{udid}] || Videos on account is deleted!')