from icecream import ic
import logging
import sys
import os
from datetime import datetime

import wda
udid = '00008030-000D05341E3B802E'
d = wda.USBClient(udid)

d.appium_settings({'snapshotMaxDepth': 17, 'maxTypingFrequency': 20})

print(d.visible_source())
d.visible_click('connect')

# if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
# else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
#
# logs_path = os.path.join(local_path, 'Logs')
# folders = [os.path.join(logs_path, d) for d in os.listdir(logs_path) if os.path.isdir(os.path.join(logs_path, d))]
# latest_folder = max(folders, key=lambda f: os.path.getctime(f))
# print(latest_folder)
# if folders:
#     print('YES')
#     name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     print(f'{local_path}/Logs/{latest_folder}/{name}.png')
#     d = wda.USBClient(udid)
#     print('YES 1')
#     d.screenshot(f'{latest_folder}/{name}.png')
#     print('YES 2')
#     print(f'{latest_folder}/{name}.png')
#     print('YES 3')
#     source_data = d.source()
#     with open(f'{latest_folder}/{name}_page.txt', 'w', encoding='utf-8') as f: f.write(source_data)
#     print('YES 4')