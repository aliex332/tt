from time import sleep
import flet as ft
import sys
import os
import platform
import shutil

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')


def main(page: ft.Page):
    # Set window size and theme
    page.window.width = 512
    page.window.height = 400
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = True
    page.window.full_screen = False
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#191919"
    page.title = "Install..."
    page.window.icon = f'{local_path}/resource/assets/photo/logo1.ico'

    pr = ft.ProgressBar(width=400, color='red')

    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Installing, please wait...", style="headlineSmall"),
                            pr,
                            ft.Text('This is the first launch. It takes around 10 minutes.\n'
                                    'Depending of your internet speed and computer power.',
                                    size=12,
                                    weight=ft.FontWeight.NORMAL,
                                    text_align="center",
                                    color=ft.Colors.WHITE,  # Для контраста с фоном
                                    ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Центрирование по вертикали
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Центрирование по горизонтали
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Центрирование Row по горизонтали
                vertical_alignment=ft.CrossAxisAlignment.CENTER  # Центрирование Row по вертикали
            ),
            expand=True,  # Контейнер будет расширяться по доступному пространству
            padding=ft.Padding(top=0, left=0, bottom=25, right=0)
        )
    )

    from cprint import cprint

    cprint.warn(f'START: App installing!')

    for i in range(0, 4):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import email
    print(f"email module loaded: {email}")

    for i in range(4, 8):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import imaplib
    print(f"imaplib module loaded: {imaplib}")

    for i in range(8, 12):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import requests
    print(f"requests module loaded: {requests}")

    for i in range(12, 16):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from datetime import datetime
    print(f"datetime module loaded: {datetime}")

    for i in range(16, 20):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from traceback import extract_stack
    print(f"traceback module loaded: {extract_stack}")

    for i in range(20, 24):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from cprint import cprint
    print(f"cprint module loaded: {cprint}")

    for i in range(24, 28):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from icecream import ic
    print(f"icecream module loaded: {ic}")

    for i in range(28, 32):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from tqdm import tqdm
    print(f"tqdm module loaded: {tqdm}")

    for i in range(32, 36):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw
    print(f"PIL modules loaded: {Image}, {ImageEnhance}, {ImageFilter}, {ImageOps}, {ImageDraw}")

    for i in range(36, 40):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from lxml import etree
    print(f"lxml module loaded: {etree}")

    for i in range(40, 44):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import numpy as np
    print(f"numpy module loaded: {np}")

    for i in range(44, 48):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import cv2
    print(f"cv2 module loaded: {cv2}")

    for i in range(48, 52):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import io
    print(f"io module loaded: {io}")

    for i in range(52, 56):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import platform
    print(f"platform module loaded: {platform}")

    for i in range(56, 60):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import pytesseract
    print(f"pytesseract module loaded: {pytesseract}")

    for i in range(60, 64):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    from urllib import request
    print(f"urllib.request module loaded: {request}")

    for i in range(64, 68):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import wda
    print(f"wda module loaded: {wda}")

    for i in range(68, 72):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import random
    print(f"random module loaded: {random}")

    for i in range(72, 76):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import subprocess
    print(f"subprocess module loaded: {subprocess}")

    for i in range(76, 80):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import base64
    print(f"base64 module loaded: {base64}")

    for i in range(80, 84):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import threading
    print(f"threading module loaded: {threading}")

    for i in range(84, 88):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import json
    print(f"json module loaded: {json}")

    for i in range(88, 92):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import re
    print(f"re module loaded: {re}")

    for i in range(92, 96):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    import shutil
    print(f"shutil module loaded: {shutil}")

    from UI_INTERFACE.MainMenu import MainMenuPage
    from UI_INTERFACE.LoginMode import LoginModePage
    from UI_INTERFACE.UploadMode import UploadModePage
    from UI_INTERFACE.ActionMode import ActionModePage
    from UI_INTERFACE.SetupDevice import SetupDevicePage
    from UI_INTERFACE.RegisterMode import RegisterModePage

    print(f"ui module loaded: {MainMenuPage}\n{LoginModePage}\n{UploadModePage}\n{ActionModePage}\n{SetupDevicePage}\n{RegisterModePage}")

    for i in range(96, 101):
        pr.value = i * 0.01
        page.update()
        sleep(0.1)

    if platform.system() == "Darwin":
        files = {
            "ios": f"{local_path}/resource/MacOS/ios",
            "backup_tool": f"{local_path}/resource/MacOS/idevicebackup2",
            "copy_tool": f"{local_path}/resource/MacOS/afcclient",
            "install_tool": f"{local_path}/resource/MacOS/ideviceinstaller"
        }
        for name, file_path in files.items():
            if os.access(file_path, os.X_OK): pass
            else: os.chmod(file_path, 0o755)

    cprint.info(f'DONE: App is successfully installed!')

    page.window.close()

def Install(): ft.app(main)