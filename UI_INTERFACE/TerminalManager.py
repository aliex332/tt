import subprocess
import platform
import ctypes
import os
from time import sleep

def mac_hide_terminal():
    os.system('')
    print("\033[2J\033[H", end="")
    applescript = '''
    tell application "Terminal"
        set miniaturized of windows to true
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])

def mac_show_terminal():
    os.system('')
    print("\033[2J\033[H", end="")
    applescript = '''
    tell application "Terminal"
        repeat with win in windows
            if miniaturized of win is true then
                set miniaturized of win to false
            end if
        end repeat
        activate
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])

def windows_hide_terminal():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0: os.system('cls'); ctypes.windll.user32.ShowWindow(hwnd, 0)
    ctypes.windll.user32.EnableMenuItem(ctypes.windll.user32.GetSystemMenu(hwnd, False), 0xF060, 0x00000001)
    ctypes.windll.user32.DrawMenuBar(hwnd)

def windows_show_terminal():
    if platform.system() == "Windows":
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0: os.system('cls'); ctypes.windll.user32.ShowWindow(hwnd, 1)

def TerminalHide():
    if platform.system() == "Windows": windows_hide_terminal()
    if platform.system() == "Darwin": mac_hide_terminal()

def TerminalShow():
    if platform.system() == "Windows": windows_show_terminal()
    if platform.system() == "Darwin": mac_show_terminal()