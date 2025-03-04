import os
import cv2
import wda
import sys
import json
import random
import requests
import platform
import subprocess
from PIL import Image
from time import sleep
from tqdm import tqdm
from cprint import cprint
from requests.auth import HTTPProxyAuth
from icecream import ic

sys.stdout.reconfigure(line_buffering=True)

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

if platform.system() == "Windows":
    ios_path = f"{local_path}/resource/Windows/ios.exe"
    backup_tool = f"{local_path}/resource/Windows/idevicebackup2.exe"
    copy_tool = f"{local_path}/resource/Windows/afcclient.exe"
    install_tool = f"{local_path}/resource/Windows/ideviceinstaller.exe"

if platform.system() == "Darwin":
    ios_path = f"{local_path}/resource/MacOS/ios"
    backup_tool = f"{local_path}/resource/MacOS/idevicebackup2"
    copy_tool = f"{local_path}/resource/MacOS/afcclient"
    install_tool = f"{local_path}/resource/MacOS/ideviceinstaller"
    files = {
        "ios": f"{local_path}/resource/MacOS/ios",
        "backup_tool": f"{local_path}/resource/MacOS/idevicebackup2",
        "copy_tool": f"{local_path}/resource/MacOS/afcclient",
        "install_tool": f"{local_path}/resource/MacOS/ideviceinstaller"
    }
    for name, file_path in files.items():
        if os.access(file_path, os.X_OK): pass
        else: os.chmod(file_path, 0o755)

def iPhone_Status(udid):
    for device_udid in json.loads(subprocess.run([ios_path, 'list'], capture_output=True, text=True, timeout=5).stdout.splitlines()[-1])['deviceList']:
        if device_udid == udid: return True
    return False

def iPhoneNetworkReset(udid):
    cprint.warn(f'[{udid}] || START: Resetting network on your iPhone...')
    iPhone_ConnectPC(udid)
    iPhone_UninstallApp(udid, 'com.zhiliaoapp.musically')
    d = wda.USBClient(udid=udid)
    reset_error = 0
    subprocess.run([ios_path, 'httpproxy', 'remove', f'--udid={udid}'], capture_output=True, text=True, timeout=30)
    while not d(name='Reset Network Settings').exists:
        if d.alert.exists:
            d.alert.click_exists('OK')
            d.alert.click_exists('Allow')
            d.alert.click_exists('Allow Full Access')
            d.alert.click_exists('Ask App Not to Track')
            d.alert.click_exists('Trust')
            d.alert.click_exists('Dismiss')

        d.app_stop('com.apple.Preferences')
        sleep(0.5)
        d.open_url("App-prefs:General&path=Reset")
        if d(type='XCUIElementTypeSearchField').exists:
            d(type='XCUIElementTypeSearchField').click_exists()
            if d.visible_click_exists('Transfer'): d(name='Reset').wait(2)
            else:
                d(type='XCUIElementTypeSearchField').get().set_text('Reset network')
                sleep(0.5)
                d.visible_click_exists('General')

        d(name='Reset').wait(2)
        d(name='Reset').click_exists()

        reset_error += 1
        if reset_error == 10: cprint.fatal(f'[{udid}] || iPhone Reset Network is not available!'); return False

    if d.alert.exists:
        d.alert.click_exists('OK')
        d.alert.click_exists('Allow')
        d.alert.click_exists('Allow Full Access')
        d.alert.click_exists('Ask App Not to Track')
        d.alert.click_exists('Trust')
        d.alert.click_exists('Dismiss')

    d(name='Reset Network Settings', visible=True).click_exists()
    sleep(2)
    d(name='Reset Network Settings', visible=True).click_exists()
    sleep(30)
    cprint.info(f'[{udid}] || DONE: iPhone network has been successfully reset!')

def iPhone_ConnectPC(udid, first_launch=False):
    cprint.warn(f'[{udid}] || START: Connecting iPhone to your PC...')
    device_offline = 0
    while True:
        try:
            for device_udid in json.loads(subprocess.run([ios_path, 'list'], capture_output=True, text=True, timeout=5).stdout.splitlines()[-1])['deviceList']:
                if device_udid == udid: print(f'[{udid}] || iPhone is online!'); break
            
            if device_udid != udid:
                print(f'[{udid}] || iPhone is offline!')
                sleep(5)
                device_offline += 1
                if device_offline == 10: return False
                continue
            
            try:
                if json.loads(subprocess.run([ios_path, 'pair', f'--p12file={local_path}/resource/Certificate/DisableTrust.p12', '--password=a', f'--udid={udid}'], capture_output=True, text=True, timeout=10).stderr.splitlines()[-1])['msg'] == f'Successfully paired {udid}': print(f'[{udid}] || iPhone is paired!')
                else: print(f'[{udid}] || Error pairing iPhone. Try again...')
            except: pass
            
            if subprocess.run([ios_path, 'devmode', 'get', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stdout.splitlines()[0] == 'Developer mode enabled: false':
                print(f'[{udid}] || iPhone DevMode is disabled! Try to enable...')
                subprocess.run([ios_path, 'devmode', 'enable', '--enable-post-restart', f'--udid={udid}'], capture_output=True, text=True, timeout=120)
                sleep(5)
                print(f'[{udid}] || iPhone DevMode is successfully enabled!')
            
            if 'WebDriverAgentRunner-Runner' in subprocess.run([ios_path, 'ps', f'--udid={udid}'], capture_output=True, text=True, timeout=20).stdout: print(f'[{udid}] || WebDriver is already launched!'); wda.USBClient(udid=udid).unlock(); cprint.info(f'[{udid}] || DONE: iPhone is successfully connected to your PC!'); return True
            
            if json.loads(subprocess.run([ios_path, 'image', 'auto', '--basedir=./resource', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] == 'success mounting image':
                result = subprocess.run([ios_path, 'apps', '--list', f'--udid={udid}'], capture_output=True, text=True, timeout=20)
                if 'com.automated.WebDriverAgentRunner.xctrunner' in result.stdout: print(f'[{udid}] || WebDriver is already installed!')
                else:
                    print(f'[{udid}] || WebDriver is not installed!')
                    if json.loads(subprocess.run([ios_path, 'install', f'--path={local_path}/resource/IPA/WDA.ipa', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] == 'installation successful':
                        print(f'[{udid}] || WebDriver is installed!')
                        sleep(2)
                    else: print(f'[{udid}] || Error installing WebDriver. Try again...')

                subprocess.run([ios_path, 'tunnel', 'stopagent'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                subprocess.Popen([ios_path, 'tunnel', 'start', '--userspace'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                sleep(5)

                print(f'[{udid}] || iOS Tunnel is created.')
                
                if json.loads(subprocess.run([ios_path, 'launch', 'com.automated.WebDriverAgentRunner.xctrunner', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] == 'Process launched':
                    print(f'[{udid}] || WebDriver is launched!')
                    sleep(5)
                else: print(f'[{udid}] || Error launching WebDriver. Try again...')
                
                if json.loads(subprocess.run([ios_path, 'launch', 'com.apple.Preferences', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] == 'Process launched':
                    sleep(2)
                    try:
                        d = wda.USBClient(udid=udid)
                        if d.alert.exists:
                            d.alert.click_exists('OK')
                            d.alert.click_exists('Allow')
                            d.alert.click_exists('Allow Full Access')
                            d.alert.click_exists('Ask App Not to Track')
                            d.alert.click_exists('Cancel')
                            d.alert.click_exists('Trust')
                            buttons = d.alert.buttons()
                            d.alert.click_exists(buttons[0])
                        if first_launch: d(nameMatches='Sign in').click_exists()
                    except RuntimeError as e: continue
                    cprint.info(f'[{udid}] || DONE: iPhone has been successfully connected to your PC!')
                    return True
            else: print(f'[{udid}] || Error mounting developer image. Try again...')
        except: continue

def iPhoneReset(udid):
    cprint.warn(f'[{udid}] || START: Hard resetting your iPhone...')
    device_offline = 0
    while True:
        try:
            for device_udid in json.loads(subprocess.run([ios_path, 'list'], capture_output=True, text=True, timeout=5).stdout.splitlines()[-1])['deviceList']:
                if device_udid == udid: print(f'[{udid}] || iPhone is online!'); break

            if device_udid != udid:
                print(f'[{udid}] || iPhone is offline!')
                sleep(5)
                device_offline += 1
                if device_offline == 10: return False
                continue

            if json.loads(subprocess.run([ios_path, 'activate', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] in ["device successfully activated", "the device is already activated"]: print(f'[{udid}] || iPhone is successfully activated!')
            else: print(f'[{udid}] || Error activation your iPhone. Try again...')

            if subprocess.run([ios_path, 'erase', '--force', f'--udid={udid}'], capture_output=True, text=True, timeout=300).stderr.splitlines()[-1] == '"ok"':
                print(f'[{udid}] || iPhone erasing is start! It takes 3-minutes, please wait...')
                for _ in tqdm(range(180), desc="Erasing", ncols=100): sleep(1)
                break
            else: print(f'[{udid}] || Error erasing your iPhone. Try again...')
        except: pass

    cprint.info(f'[{udid}] || DONE: iPhone has been successfully erased!')
    sleep(0.5)

    cprint.warn(f'[{udid}] || START: Setting up your iPhone...')
    device_offline = 0
    while True:
        try:
            for device_udid in json.loads(subprocess.run([ios_path, 'list'], capture_output=True, text=True, timeout=5).stdout.splitlines()[-1])['deviceList']:
                if device_udid == udid: break

            if device_udid != udid:
                print(f'[{udid}] || iPhone is offline!')
                sleep(5)
                device_offline += 1
                if device_offline == 10: return False
                continue

            if json.loads(subprocess.run([ios_path, 'activate', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] in ["device successfully activated", "the device is already activated"]:
                if json.loads(subprocess.run([ios_path, 'profile', 'add', f'{local_path}/resource/Certificate/WiFi.mobileconfig', f'--udid={udid}'], capture_output=True, text=True, timeout=10).stderr.splitlines()[-1])['msg'] in ["profile installed, you have to accept it in the device settings"]: print(f'[{udid}] || iPhone Wi-Fi is successfully connected!')
                else: sleep(5); continue
                print(f'[{udid}] || Preparing setup for your iPhone. Please wait...')

                folders = [f for f in os.listdir(f'{local_path}/resource/Backup') if os.path.isdir(os.path.join(f'{local_path}/resource/Backup', f))]
                os.rename(f'{local_path}/resource/Backup/{folders[0]}', f'{local_path}/resource/Backup/{udid}')

                subprocess.check_output([backup_tool, 'restore', '--settings', '--system', '--remove', f'{local_path}/resource/Backup', f'--udid={udid}'])

                print(f'[{udid}] || iPhone setup is start! It takes 3-minutes, please wait...')
                sleep(0.5)
                for _ in tqdm(range(180), desc="Setup", ncols=100): sleep(1)
                break
            else: print(f'[{udid}] || Error activation your iPhone. Try again...')
        except: pass


    device_offline = 0
    while True:
        device_offline += 1
        if device_offline == 10: return False
        if subprocess.run([ios_path, 'devmode', 'get', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stdout.splitlines()[0] == 'Developer mode enabled: false':
            print(f'[{udid}] || iPhone DevMode is disabled! Try to enable, please wait...')
            subprocess.run([ios_path, 'devmode', 'enable', '--enable-post-restart', f'--udid={udid}'], capture_output=True, text=True, timeout=120)
            sleep(5)
            print(f'[{udid}] || iPhone DevMode is successfully enabled!')
            cprint.info(f'[{udid}] || DONE: iPhone has been successfully set up!')

        if subprocess.run([ios_path, 'devmode', 'get', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stdout.splitlines()[0] == 'Developer mode enabled: true':
            if json.loads(subprocess.run([ios_path, 'profile', 'add', f'{local_path}/resource/Certificate/WiFi.mobileconfig', f'--p12file={local_path}/resource/Certificate/DisableTrust.p12', '--password=a', f'--udid={udid}'], capture_output=True, text=True, timeout=10).stderr.splitlines()[-1])['msg'] in ["profile installed"]: print(f'[{udid}] || iPhone Wi-Fi is successfully connected!')
            else: print(f'[{udid}] || Error Wi-Fi connection failed! Try again...'); continue
            return True
        else: print(f'[{udid}] || Error enabling DevMode. Try again...')

def iPhone_CopyPhotoVideo(d, udid, video_mode, photo_count=None):
    def is_video_valid(file_path):
        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened(): return False
            ret, _ = cap.read()  # Попытка прочитать первый кадр
            cap.release()
            return ret
        except Exception as e: return False

    def is_image_valid(file_path):
        try:
            with Image.open(file_path) as img: img.verify(); return True
        except Exception as e: return False

    bundle_id = d.app_current().get("bundleId")
    iPhone_Shortcut(d, udid, mode='Delete')

    subprocess.check_output([copy_tool, '--documents', 'com.automated.WebDriverAgentRunner.xctrunner', 'mkdir', '/Documents/Gallery', f'--udid={udid}'])

    if video_mode in ['Video', 'Overlay']:
        if video_mode == 'Video': folder_path = f'{local_path}/iPhoneTikTokFiles/Videos/'
        if video_mode == 'Overlay': folder_path = f'{local_path}/iPhoneTikTokFiles/Overlay/Video/'
        while True:
            video_folders = os.listdir(folder_path)
            if not video_folders: cprint.fatal(f'[{udid}] || ERROR: {video_mode} folder is empty! To continue working, please add new videos to this folder. Checking again in 1 minute...'); sleep(60); continue
            random.shuffle(video_folders)
            video_file = f'{folder_path}{video_folders[0]}'
            if not is_video_valid(video_file): cprint.fatal(f'[{udid}] || Video {video_file} is corrupted. Removing...'); os.remove(video_file); continue
            subprocess.check_output([copy_tool, '--documents', 'com.automated.WebDriverAgentRunner.xctrunner', 'put', f'{video_file}', f'/Documents/Gallery/{video_folders[0]}', f'--udid={udid}'])
            if video_mode != 'Overlay': os.remove(video_file)
            break

    if video_mode in ['Photo', 'Autocut', 'Avatar']:
        if video_mode == 'Photo': count_photo = photo_count; folder_path = f'{local_path}/iPhoneTikTokFiles/Photos/'
        if video_mode == 'Autocut': count_photo = photo_count; folder_path = f'{local_path}/iPhoneTikTokFiles/Autocut/'
        if video_mode == 'Avatar': count_photo = 1; folder_path = f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Avatars/'

        for count in range(count_photo):
            while True:
                try:
                    photo_folders = os.listdir(folder_path)
                    if not photo_folders: cprint.fatal(f'[{udid}] || ERROR: {video_mode} folder is empty! To continue working, please add new videos to this folder. Checking again in 1 minute...'); sleep(60); continue
                    random.shuffle(photo_folders)
                    photo_file = f'{folder_path}{photo_folders[0]}'
                    if not is_image_valid(photo_file): cprint.fatal(f'[{udid}] || ERROR: Photo {photo_file} is corrupted. Removing...'); os.remove(photo_file); continue
                    _, file_extension = os.path.splitext(photo_file)
                    subprocess.check_output([copy_tool, '--documents', 'com.automated.WebDriverAgentRunner.xctrunner', 'put', f'{photo_file}', f'/Documents/Gallery/{count}{file_extension}', f'--udid={udid}'])
                    if video_mode == 'Photo': os.remove(photo_file)
                except: continue
                break

        if video_mode == 'Video': cprint.info(f'[{udid}] || DONE: Video has been copied to the iPhone!')
        if video_mode == 'Photo': cprint.info(f'[{udid}] || DONE: Photo has been copied to the iPhone!')
        if video_mode == 'Avatar': cprint.info(f'[{udid}] || DONE: Avatar has been copied to the iPhone!')
        if video_mode == 'Overlay': cprint.info(f'[{udid}] || DONE: Overlay has been copied to the iPhone!')
        if video_mode == 'Autocut': cprint.info(f'[{udid}] || DONE: Autocut photos have been copied to the iPhone!')

    iPhone_Shortcut(d, udid, mode='Save')
    d.app_start(bundle_id)

def iPhone_CopyFile(udid, file_path, iphone_path, app_name):
    subprocess.check_output([copy_tool, '--documents', f'{app_name}', 'put', f'{file_path}', f'{iphone_path}', f'--udid={udid}'])

def iPhone_Proxy(d, udid, country_code, proxy=None):
    def check_proxy(proxy_ip, proxy_port, proxy_login, proxy_pass):
        proxy_url = f"http://{proxy_ip}:{proxy_port}"
        proxies = {"http": proxy_url, "https": proxy_url}
        auth = HTTPProxyAuth(proxy_login, proxy_pass)  # Аутентификация через прокси
        try:
            response = requests.get("http://www.tiktok.com", proxies=proxies, auth=auth, timeout=5)
            if response.status_code == 200: return True
            else: return False
        except requests.exceptions.RequestException: return False


    cprint.warn(f'[{udid}] || START: Connecting iPhone to Proxy...')
    if proxy != None:
        parts = proxy.strip().split(':')
        proxy_ip = parts[1]
        proxy_port = parts[2]
        proxy_login = parts[3]
        proxy_pass = parts[4]
        if check_proxy(proxy_ip, proxy_port, proxy_login, proxy_pass) is True:
            print(f'[{udid}] || Proxy online: {proxy_ip}:{proxy_port}!')
            if json.loads(subprocess.run([ios_path, 'httpproxy', proxy_ip, proxy_port, proxy_login, proxy_pass, f'--p12file={local_path}/resource/Certificate/DisableTrust.p12', '--password=a', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] == 'success':
                try:
                    d.alert.wait(5)
                    d.alert.accept()
                    sleep(1)
                    d(value='Username').get().set_text(proxy_login)
                    d(value='Password').get().set_text(proxy_pass)
                    d.alert.accept()
                except: pass
            else: print(f'[{udid}] || Error with connecting to Proxy!')
            cprint.info(f'[{udid}] || DONE: Proxy has successfully connected on your iPhone!')
            return f'PROXY:{proxy_ip}:{proxy_port}:{proxy_login}:{proxy_pass}'
        cprint.fatal(f'[{udid}] || ERROR: Proxy offline: {proxy_ip}:{proxy_port}!')

    with open(f'{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/Proxy/Proxy.txt', 'r') as file:
        for line in file:
            # Разбиваем строку по двоеточию
            parts = line.strip().split(':')

            # Проверяем, если страна (первый элемент) совпадает с нужной
            if parts[0] == country_code:  # Замените 'GB' на страну, которую ищете
                proxy_ip = parts[1]
                proxy_port = parts[2]
                proxy_login = parts[3]
                proxy_pass = parts[4]

                if check_proxy(proxy_ip, proxy_port, proxy_login, proxy_pass) is True:
                    print(f'[{udid}] || Proxy online: {proxy_ip}:{proxy_port}!')
                    if json.loads(subprocess.run([ios_path, 'httpproxy', proxy_ip, proxy_port, proxy_login, proxy_pass, f'--p12file={local_path}/resource/Certificate/DisableTrust.p12', '--password=a', f'--udid={udid}'], capture_output=True, text=True, timeout=30).stderr.splitlines()[-1])['msg'] == 'success': print(f'[{udid}] || Proxy connected!')
                    else: print(f'[{udid}] || Error with connecting to Proxy!')
                    try:
                        d.alert.wait(5)
                        d.alert.accept()
                        sleep(1)
                        d(value='Username').get().set_text(proxy_login)
                        d(value='Password').get().set_text(proxy_pass)
                        d.alert.accept()
                    except: pass
                    cprint.info(f'[{udid}] || DONE: Proxy has successfully connected on your iPhone!')
                    return f'PROXY:{proxy_ip}:{proxy_port}:{proxy_login}:{proxy_pass}'
                cprint.fatal(f'[{udid}] || ERROR: Proxy offline: {proxy_ip}:{proxy_port}!')
    cprint.fatal(f'[{udid}] || ERROR: All proxies are offline, or no proxy found for {country_code} in your list. Please check your file and try again...')
    return False

def iPhone_SetRegion(udid, country_code):
    country_code = GetLocale(country_code)
    if country_code is None: print(f'[{udid}] || ERROR: Region does not exist!'); return True
    subprocess.run([ios_path, 'lang', f'--setlocale=', f'--udid={udid}'], capture_output=True, text=True, timeout=30)
    sleep(1)
    subprocess.run([ios_path, 'lang', f'--setlocale=', f'--udid={udid}'], capture_output=True, text=True, timeout=30)
    sleep(1)
    subprocess.run([ios_path, 'lang', f'--setlocale={country_code}', f'--udid={udid}'], capture_output=True, text=True, timeout=30)
    print(f'[{udid}] || DONE: Region and timezone have been changed to: {country_code}!')


def iPhone_InstallApp(udid, path):
    bad_install = 0
    while True:
        try:
            if 'Complete' in subprocess.check_output([install_tool, 'install', f'{path}', f'--udid={udid}'], stderr=subprocess.PIPE, text=True, timeout=90): print(f"[{udid}] || App successfully installed!"); return True
        except: print(f'[{udid}] || Error installing the app. Try again...')
        bad_install += 1
        if bad_install >= 5: print(f"[{udid}] || ERROR: App installation failed multiple times."); return False

def iPhone_UninstallApp(udid, bundle_id):
    bad_uninstall = 0
    while True:
        if 'Complete' in subprocess.check_output([install_tool, 'uninstall', f'{bundle_id}', f'--udid={udid}'], stderr=subprocess.PIPE, text=True, timeout=90): print(f"[{udid}] || App uninstalled successfully!"); return True
        else: print(f'[{udid}] || Error uninstalling the app. Try again...')
        bad_uninstall += 1
        if bad_uninstall >= 5: print(f"[{udid}] || ERROR: App uninstalling failed multiple times."); return False

def iPhone_MobileNetwork(d, udid):
    d.open_url("App-prefs:WIFI")
    sleep(2)
    if d(type='XCUIElementTypeSwitch', value=1).exists: d(type='XCUIElementTypeSwitch').click()
    cprint.info(f'[{udid}] || DONE: Mobile network has been enabled on your iPhone!')

def iPhone_Shortcut(d, udid, mode):
    if mode == 'Profile': d.open_url('shortcuts://run-shortcut?name=Profile')
    if mode == 'Record': d.open_url('shortcuts://run-shortcut?name=Record')
    if mode == 'Delete': d.open_url('shortcuts://run-shortcut?name=Delete')
    if mode == 'Save': d.open_url('shortcuts://run-shortcut?name=Save')

    d(name='junior_platter_view').wait(2)
    while d(name='junior_platter_view').exists:
        d(type='XCUIElementTypeButton', name='Delete Always').click_exists()
        d(type='XCUIElementTypeButton', name='Always Allow').click_exists()
        d(type='XCUIElementTypeButton', name='Allow').click_exists()
        d(type='XCUIElementTypeButton', name='OK').click_exists()
        d(name='junior_platter_view').wait(2)



def Create_WiFiconfig(login, password):
    if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
    else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
    if len(login) == 0: return False

    mobileconfig_content = f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
<plist version=\"1.0\">
    <dict>
        <key>PayloadContent</key>
        <array>
            <dict>
                <key>allowUnpairedExternalBootToRecovery</key>
                <true />
                <key>PayloadDisplayName</key>
                <string>Restrictions</string>
                <key>PayloadIdentifier</key>
                <string>com.apple.applicationaccess.125db813-fe1a-40ba-b66c-86c77d6a791b</string>
                <key>PayloadType</key>
                <string>com.apple.applicationaccess</string>
                <key>PayloadUUID</key>
                <string>ded8525f-714c-4978-82fc-dd9f554c0c71</string>
                <key>PayloadVersion</key>
                <integer>1</integer>
            </dict>
            <dict>
                <key>EncryptionType</key>
                <string>WPA</string>
                <key>Interface</key>
                <string>AnyEthernet</string>
                <key>Password</key>
                <string>{password}</string>
                <key>PayloadDisplayName</key>
                <string>Wi-Fi #1</string>
                <key>PayloadIdentifier</key>
                <string>com.apple.wifi.managed.104a7ebe-20e2-4b24-bd36-1cb6246018ec</string>
                <key>PayloadType</key>
                <string>com.apple.wifi.managed</string>
                <key>PayloadUUID</key>
                <string>57222f7f-8604-44ab-acb9-0e208a7e4910</string>
                <key>PayloadVersion</key>
                <integer>1</integer>
                <key>SSID_STR</key>
                <string>{login}</string>
            </dict>
        </array>
        <key>PayloadDisplayName</key>
        <string>WiFi</string>
        <key>PayloadIdentifier</key>
        <string>DESKTOP-41USB31.4d6e6a17-1f94-4ee1-9fbe-ec6d7913ed1e</string>
        <key>PayloadType</key>
        <string>Configuration</string>
        <key>PayloadUUID</key>
        <string>a73e1849-686c-46bf-bc34-1e8cb78a6759</string>
        <key>PayloadVersion</key>
        <integer>1</integer>
    </dict>
</plist>
"""

    with open(f'{local_path}/resource/Certificate/WiFi.mobileconfig', 'w') as file: file.write(mobileconfig_content)
    return True

def GetLocale(country_code):
    supported_locales = [
        "ro_RO", "en_VG", "es_VC", "fr_MA", "en_AL", "es_TT",
        "ar_SS", "fr_VU", "fr_CI", "en_BW", "en_JM", "es_BS", "en_BD", "en_MG",
        "en_PT", "ar_LB", "ru_UA", "en_HK", "fr_GN", "en_CO", "en_KE", "en_NR",
        "fr_MU", "en_FI", "nl_BQ", "en_WS", "en_DG", "ar_SA", "en_RW", "en_ZM",
        "en_BE", "el_CY", "en_MH", "en_ER", "nl_NL", "pt_AO", "en_KY", "es_CL",
        "en_VI", "es_VE", "en_FJ", "fr_MC", "en_TZ", "en_ID", "es_TC", "zh_TW",
        "en_GU", "es_GQ", "ko_CN", "en_GB", "es_MX", "es_BB", "es_PR", "fr_GP",
        "pt_GW", "fi_FI", "en_FK", "en_NA", "zh_CN", "en_IE", "ca_IT", "en_TH",
        "en_LR", "ar_KM", "en_BZ", "de_CH", "da_GL", "en_JP", "en_BG", "en_US",
        "ar_QA", "en_PW", "ar_TN", "fr_GQ", "de_LI", "cs_CZ", "hu_HU", "zh_HK",
        "en_NU", "es_VG", "ar_EG", "ro_MD", "en_LS", "fr_CM", "ar_SD", "en_GD",
        "ar_IL", "ar_LY", "en_UA", "fr_TD", "pt_LU", "es_PA", "en_KI", "es_CO",
        "en_FM", "fr_MF", "tr_CY", "ar_EH", "en_LT", "es_IC", "en_DK", "pt_ST",
        "es_GT", "fr_YT", "ms_BN", "en_BI", "he_IL", "pt_TL", "en_SS", "es_KY",
        "kk_KZ", "en_CA", "es_VI", "zh-Hant_JP", "fr_MG", "ar_MR", "hr_HR",
        "en_AR", "ar_SY", "en_TK", "fr_SN", "en_GY", "pt_CV", "en_MM", "es_ES",
        "ar_AE", "fr_DZ", "en_001", "en_PG", "ca_ES", "fr_RW", "fr_GA", "en_SA",
        "fr_BE", "hi_IN", "en_AS", "pt_MO", "en_LV", "en_DM", "en_LC", "en_GG",
        "tr_TR", "es_BZ", "it_CH", "zh-Hans_MO", "es_US", "it_VA", "fr_TG",
        "en_EE", "en_150", "en_PH", "es_HN", "sv_FI", "en_CV", "ms_SG", "en_SB",
        "fr_RE", "en_CC", "fr_BF", "en_NF", "es_EA", "es_CR", "en_AT", "ar_MA",
        "nl_BE", "en_GH", "th_TH", "en_ZA", "pt_FR", "es_GD", "en_MO", "de_IT",
        "es_003", "es_PE", "de_DE", "en_NZ", "en_SC", "en_NG", "en_AU", "el_GR",
        "en_GI", "ar_001", "en_BM", "ar_IQ", "en_MP", "es_PY", "fr_DJ", "es_EC",
        "vi_VN", "en_US_POSIX", "en_CX", "en_KN", "en_SD", "en_FR", "es_CA",
        "en_IL", "es_AR", "en_TO", "zh-Hans_HK", "es_GY", "bg_BG", "fr_NC",
        "en_BN", "en_UG", "en_HU", "uk_UA", "en_SX", "en_PK", "en_CY", "en_SE",
        "es_CU", "sk_SK", "fr_BI", "fr_ML", "de_BE", "en_IM", "fr_PF", "es_DM",
        "es_LC", "en_ZW", "fr_CA", "pl_PL", "zh-Hans_JP", "nl_SR", "en_JE",
        "pt_CH", "ja_JP", "fr_LU", "en_PL", "es_PH", "en_CZ", "fr_GF", "zh_MO",
        "fr_BJ", "en_IN", "en_AE", "fr_NE", "en_MS", "es_419", "it_IT", "ar_TD",
        "en_SZ", "fr_WF", "ru_MD", "es_SV", "en_SG", "es_CW", "en_CH", "pt_BR",
        "en_IO", "ar_PS", "en_TR", "ar_KW", "es_DO", "en_GM", "it_SM", "ms_MY",
        "es_UY", "en_MT", "es_BM", "en_PN", "es_HT", "en_KR", "en_SH", "en_VU",
        "es_KN", "fr_BL", "en_NL", "ca_FR", "en_AG", "fr_KM", "fr_SC", "fr_CD",
        "ko_KP", "nb_SJ", "en_BR", "en_MU", "ru_RU", "fr_TN", "ar_DZ", "zh-Hant_CN",
        "en_SI", "hr_BA", "es_NI", "ar_ER", "en_VC", "fr_HT", "en_TT", "ar_SO",
        "ca_AD", "fr_FR", "da_DK", "en_BS", "en_MV", "es_BO", "nb_NO", "nl_CW",
        "de_LU", "en_CK", "ar_JO", "pt_GQ", "fr_MQ", "zh_SG", "ms_ID", "en_AI",
        "fr_CF", "ko_KR", "en_MW", "en_UM", "en_SK", "en_CL", "en_NO", "fr_MR",
        "en_TV", "fr_SY", "en_TC", "fr_CG", "nl_SX", "en_MX", "ar_YE", "en_BB",
        "sv_SE", "de_AT", "en_PR", "es_BQ", "ar_DJ", "ru_BY", "ar_OM", "nl_AW",
        "en_SL", "en_CM", "ru_KZ", "ar_BH", "ru_KG", "pt_MZ", "id_ID", "fr_PM",
        "en_TW", "es_AG", "pt_PT", "en_DE", "fr_CH", "en_GR", "en_RU", "en_MY",
        "es_BR"
    ]
    # Найти все подходящие локали
    matching_locales = [locale for locale in supported_locales if locale.endswith(f"_{country_code}")]

    # Если есть совпадения, вернуть случайное
    if matching_locales: return random.choice(matching_locales)
    return None