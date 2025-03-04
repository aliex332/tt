udid = '00008030-000D05341E3B802E'

import os
import sys
from UI_INTERFACE.TerminalManager import TerminalHide, TerminalShow

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

if not os.path.exists(f"{local_path}/resource/Installed.txt"):
    from UI_INTERFACE.Installing import Install
    try: Install()
    except: sys.exit()
    with open(f"{local_path}/resource/Installed.txt", "w") as file:
        file.write('')


import flet as ft
import multiprocessing
from UI_INTERFACE.MainMenu import MainMenuPage
from UI_INTERFACE.LoginMode import LoginModePage
from UI_INTERFACE.UploadMode import UploadModePage
from UI_INTERFACE.ActionMode import ActionModePage
from UI_INTERFACE.SetupDevice import SetupDevicePage
from UI_INTERFACE.RegisterMode import RegisterModePage

def ResetStorage(page: ft.Page):
    page.client_storage.clear()

def main(page: ft.Page):
    TerminalHide()
    page.window.icon = f'{local_path}/resource/assets/photo/logo1.ico'
    page.title = "TikTok by iOS EXPERT"
    def route_change(e: ft.RouteChangeEvent):
        page.controls.clear()

        if e.route == "/MainMenuPage":
            page.client_storage.clear()
            page.client_storage.set("Register", False)
            page.client_storage.set("Login", False)
            page.client_storage.set("Upload", False)
            page.client_storage.set("Mention", False)

            page.client_storage.set("account_list_laps", False)
            page.client_storage.set("mobile_network", False)
            page.client_storage.set("reset_network", False)
            page.client_storage.set("proxy_enable", False)
            page.client_storage.set("vpn_enable", False)
            page.client_storage.set("accounts_count", False)
            page.client_storage.set("country_code", False)
            page.client_storage.set("Video", False)
            page.client_storage.set("Photo", False)
            page.client_storage.set("Autocut", False)
            page.client_storage.set("Overlay", False)
            page.client_storage.set("Record", False)
            page.client_storage.set("use_music_switch", False)
            page.client_storage.set("use_again_switch", False)
            page.client_storage.set("videos_count", False)
            page.client_storage.set("photo_count", False)
            page.client_storage.set("record_time", False)
            page.client_storage.set("sleep_count", False)
            page.client_storage.set("lap_count", False)
            page.client_storage.set("nickname_change", False)
            page.client_storage.set("link_change", False)
            page.client_storage.set("bio_change", False)
            page.client_storage.set("avatar_change", False)
            page.client_storage.set("follow_account", False)
            page.client_storage.set("send_comments", False)
            page.client_storage.set("video_description", False)
            page.client_storage.set("video_hashtags", False)
            page.client_storage.set("delete_video", False)
            page.client_storage.set("delete_link", False)
            page.client_storage.set("delete_bio", False)
            page.client_storage.set("business_enable", False)
            page.client_storage.set("business_register", False)

            MainMenuPage(udid, page)

        elif e.route == "/RegisterModePage":
            page.client_storage.set("Register", True)
            page.client_storage.set("register_mode", False)
            page.client_storage.set("mobile_network", False)
            page.client_storage.set("reset_network", False)
            page.client_storage.set("proxy_enable", False)
            page.client_storage.set("vpn_enable", False)
            page.client_storage.set("accounts_count", 0)
            page.client_storage.set("country_code", [])
            RegisterModePage(page)

        elif e.route == "/LoginModePage":
            page.client_storage.set("Login", True)
            page.client_storage.set("mobile_network", False)
            page.client_storage.set("reset_network", False)
            page.client_storage.set("account_list_laps", 1)
            LoginModePage(page)

        elif e.route == "/UploadModePage":
            page.client_storage.set("UploadSkip", False)
            page.client_storage.set("Upload", True)
            page.client_storage.set("Video", False)
            page.client_storage.set("Photo", False)
            page.client_storage.set("Autocut", False)
            page.client_storage.set("Overlay", False)
            page.client_storage.set("Record", False)
            page.client_storage.set("use_music_switch", False)
            page.client_storage.set("use_again_switch", False)
            page.client_storage.set("videos_count", 6)
            page.client_storage.set("photo_count", 3)
            page.client_storage.set("record_time", 7)
            page.client_storage.set("sleep_count", 30)
            page.client_storage.set("lap_count", 3)
            UploadModePage(page)

        elif e.route == "/ActionModePage":
            page.client_storage.set("Mention", True)
            page.client_storage.set("nickname_change", {"enabled": False, "when": "Before"})
            page.client_storage.set("link_change", {"enabled": False, "when": "Before"})
            page.client_storage.set("bio_change", {"enabled": False, "when": "Before"})
            page.client_storage.set("avatar_change", False)
            page.client_storage.set("follow_account", False)
            page.client_storage.set("send_comments", False)
            page.client_storage.set("video_description", False)
            page.client_storage.set("video_hashtags", {"enabled": False, "hashtag_count": 3})
            page.client_storage.set("delete_video", False)
            page.client_storage.set("delete_link", False)
            page.client_storage.set("delete_bio", False)
            ActionModePage(udid, page)

        elif e.route == "/SetupDevice":
            SetupDevicePage(udid, page)

        page.update()

    page.on_route_change = route_change
    page.go("/MainMenuPage")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    ft.app(target=main, assets_dir='./resource/assets')