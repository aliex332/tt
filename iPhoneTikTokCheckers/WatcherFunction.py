import os
import re
import base64
import threading
from PIL import Image
from lxml import etree
from time import sleep
from cprint import cprint
from requests import post, get
from iPhoneTikTokCheckers.CaptchaCircle import CaptchaCircle
from iPhoneTikTokCheckers.CaptchaSlider import CaptchaSlider
from iPhoneTikTokCheckers.CaptchaObjects import CaptchaObjects


class Alert_Watcher:
    def __init__(self, d, udid):
        self.d = d
        self.udid = udid
        self.stop_event = threading.Event()
        self.stop_event.set()
        self.daemon_thread = None
        import sys
        if getattr(sys, 'frozen', False): self.local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
        else: self.local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    def stop(self):
        self.stop_event.set()
        if self.daemon_thread is not None: self.daemon_thread.join()
        print(f'[{self.udid}] || Pop-up disable daemon stop!')

    def start(self):
        self.stop_event.clear()
        if self.daemon_thread is None or not self.daemon_thread.is_alive():
            self.daemon_thread = threading.Thread(name='Alerts', target=self.run, daemon=True)
            self.daemon_thread.start()
            print(f'[{self.udid}] || Pop-up disable daemon start!')

    def run(self):
        while not self.stop_event.is_set():
            Watch = threading.Thread(name="watcher", target=self.WatchersStart)
            Watch.start()
            Watch.join()
            sleep(10)

    def WatchersStart(self):
        try:
            # iPHONE ALERT PERMISSIONS ---------------------------------------------------------------------------------------
            if self.d.alert.exists:
                buttons = self.d.alert.buttons()
                if len(buttons) == 1: self.d.alert.click_exists(buttons[0])
                self.d.alert.click_exists('OK')
                self.d.alert.click_exists('Allow')
                self.d.alert.click_exists('Allow Full Access')
                self.d.alert.click_exists('Ask App Not to Track')
                self.d.alert.click_exists('Cancel')
                self.d.alert.click_exists('Trust')

            if self.d.app_current().get("bundleId") == 'com.apple.shortcuts':
                self.d(name='Allow').click_exists()
                self.d(name='OK').click_exists()

            if self.d.app_current().get("bundleId") == 'com.zhiliaoapp.musically':
                source = self.d.source()
                tree = etree.fromstring(source.encode('utf-8'))

                watcher_list = [
                    ".//XCUIElementTypeStaticText[@name='When’s your birthday?' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Agree and continue' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Start watching' and @visible='true']",
                    ".//XCUIElementTypeOther[@name='verify captcha' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='I agree' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Got it' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Accept' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Allow' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Skip' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Save' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='OK' and @visible='true']",
                    ".//XCUIElementTypeStaticText[@name='Swipe up for more']",
                    ".//XCUIElementTypeStaticText[@name='Not now']"
                ]

                for watcher in watcher_list:
                    elements = tree.xpath(watcher)
                    if elements:
                        if watcher == ".//XCUIElementTypeStaticText[@name='Swipe up for more']": self.d.swipe(0.5, 0.8, 0.5, 0.1, 0.01); break
                        if watcher == ".//XCUIElementTypeStaticText[@name='When’s your birthday?' and @visible='true']":
                            picker_wheels = self.d.xpath('//XCUIElementTypePickerWheel').find_elements()
                            if picker_wheels:
                                for wheel in picker_wheels:
                                    bounds = wheel.bounds
                                    x = int(bounds.x + (bounds.width / 2))
                                    y_start = int(bounds.y + (bounds.height / 2))
                                    end_y = y_start + 150
                                    for _ in range(3): self.d.swipe(x, y_start, x, end_y, duration=0)
                            self.d(name='OK').click_exists()
                            self.d(name='Next').click_exists()
                            self.d(name='OK').click_exists()
                            self.d(name='Next').click_exists()
                            break
                        if watcher == ".//XCUIElementTypeOther[@name='verify captcha' and @visible='true']":
                            cprint.fatal(f'[{self.udid}] || Captcha is founded! Try to solving!')
                            if self.d(name='Select 2 objects that are the same shape').exists:
                                cprint.fatal(f'[{self.udid}] || Captcha objects detected!')
                                CaptchaObjects(self.d, self.udid)

                            if self.d(name='Drag the slider to fit the puzzle').exists:
                                cprint.fatal(f'[{self.udid}] || Captcha circle detected!')
                                CaptchaCircle(self.d, self.udid)

                            if self.d(name='Drag the puzzle piece into place').exists:
                                cprint.fatal(f'[{self.udid}] || Captcha slider detected!')
                                CaptchaSlider(self.d, self.udid)

                            locators_buttons = ['Log in',
                                                'Confirm',
                                                'Next',
                                                'Continue']

                            for button_name in locators_buttons:
                                try:
                                    self.d(text=button_name, visible=True).click_exists()
                                except:
                                    pass
                                sleep(0.5)
                            break

                        center_x = int(elements[0].attrib.get('x', 0)) + int(elements[0].attrib.get('width', 0)) // 2
                        center_y = int(elements[0].attrib.get('y', 0)) + int(elements[0].attrib.get('height', 0)) // 2
                        self.d.click(center_x, center_y)
                        sleep(1)
        except: pass