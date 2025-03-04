import os
import re
import sys
import random
import shutil
import wda
from icecream import ic
from time import sleep
from cprint import cprint
from datetime import datetime
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneControl.iPhoneControl import iPhone_UninstallApp, iPhone_InstallApp, iPhone_CopyFile

def ConnectVPN(d, udid, country_code, vpn_name=False):
    if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
    else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    cprint.warn(f'[{udid}] || START: Connecting iPhone to OpenVPN...')
    vpn_configs_list = os.listdir(f'{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/COUNTRY/{country_code}')
    random.shuffle(vpn_configs_list)

    for vpn_configs in vpn_configs_list:
        try:
            if not vpn_name: vpn_name_pass = re.findall(r"\w*_([\s\S]*)\.ovpn", vpn_configs)
            else:
                if vpn_name: vpn_configs = f'{vpn_name}.ovpn'; vpn_name_pass = re.findall(r"\w*_([\s\S]*)\.ovpn", vpn_configs)
            # ____________________________________________________________________________________________________________________________
            # CHOSE VPN NAME AND PASSWORD:
            with open(f'{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/VPNServices.txt') as f: lines = [line.strip() for line in f]
            for line in lines:
                vpn_name = line.split(':')
                if vpn_name[0] == vpn_name_pass[0]:
                    vpn_login = vpn_name[1]
                    vpn_pass = vpn_name[2]
                    break

            if os.path.isfile(f'{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/COUNTRY/{country_code}/{vpn_configs}') is False: continue

            iPhone_UninstallApp(udid, 'net.openvpn.connect.app')
            iPhone_InstallApp(udid, path=f'{local_path}/resource/IPA/OpenVPN.ipa')

            d.appium_settings({'snapshotMaxDepth': 17})
            d.app_start('net.openvpn.connect.app')
            source_path = f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/COUNTRY/{country_code}/{vpn_configs}"
            destination_path = f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/COUNTRY/VPN.ovpn"

            # Копируем файл
            shutil.copy(source_path, destination_path)

            # Заменяем auth-user-pass
            with open(destination_path, "r", encoding="utf-8") as file: content = file.read()
            content = content.replace("auth-user-pass", f"""<auth-user-pass>\n{vpn_login}\n{vpn_pass}\n</auth-user-pass>""")
            with open(destination_path, "w", encoding="utf-8") as file: file.write(content)


            iPhone_CopyFile(udid, file_path=f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/COUNTRY/VPN.ovpn", iphone_path=f'/Documents/VPN.ovpn', app_name='net.openvpn.connect.app')
            timer = datetime.now()
            while d.visible_click_exists('ADD') is None:
                if BadTimer(udid, timer, 15) is False: break
                print(d.alert.exists)
                d.alert.click_exists('Allow')
                d(name='AGREE').click_exists()

            for _ in range(30):
                d.visible_click_exists('ADD')
                d.visible_button_click_exist('orange')
                d.alert.click_exists('Allow')
                if d.visible_click_exists('CONNECTED'):
                    vpn_configs = vpn_configs.replace(".ovpn", "")
                    cprint.info(f'[{udid}] || DONE: OpenVPN has been successfully set up! VPN: {vpn_configs}')
                    d.appium_settings({'snapshotMaxDepth': 17})
                    return f'VPN:{vpn_configs}'
                d.visible_click_exists('OK')

            if d.visible_click_exists('CONNECTED') is None or d.visible_click_exists('Failed').exists:
                if vpn_name: vpn_name = False
                d.appium_settings({'snapshotMaxDepth': 17})
                continue

        except: d.appium_settings({'snapshotMaxDepth': 17}); sleep(2); continue

    return False