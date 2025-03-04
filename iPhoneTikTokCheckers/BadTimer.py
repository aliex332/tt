from time import sleep
from cprint import cprint
from datetime import datetime
from lxml import etree


def BadTimer(udid, time_now, max_timer, trace, line, d=None):
    timer_count = (datetime.now() - time_now).seconds
    if timer_count > max_timer:
        cprint.fatal(f'[{udid}] || Timeout! Function name: {trace}(). Line number: {line}')
        return False

    if d is not None:
        try:
            while True:
                found = False  # Флаг, указывающий, что было найдено что-то для обработки

                # Обработка алертов
                if d.alert.exists:
                    found = (
                            d.alert.click_exists('Ask App Not to Track') or
                            d.alert.click_exists('Allow Full Access') or
                            d.alert.click_exists('Allow') or
                            d.alert.click_exists('OK') or
                            d.alert.click_exists('Cancel')
                            ) or found  # Устанавливаем found в True, если был клик по любому алерту

                # Проверяем текущий бандл ID приложения
                if d.app_current().get("bundleId") == 'com.zhiliaoapp.musically':
                    source = d.source()
                    tree = etree.fromstring(source.encode('utf-8'))

                    watcher_list = [
                        ".//XCUIElementTypeStaticText[@name='Agree and continue' and @visible='true']",
                        ".//XCUIElementTypeStaticText[@name='Start watching' and @visible='true']",
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
                            found = True  # Устанавливаем found в True, если элемент найден
                            if watcher == ".//XCUIElementTypeStaticText[@name='Swipe up for more']":
                                d.swipe(0.5, 0.8, 0.5, 0.1, 0.01)
                                break

                            # Вычисляем координаты элемента для клика
                            center_x = int(elements[0].attrib.get('x', 0)) + int(elements[0].attrib.get('width', 0)) // 2
                            center_y = int(elements[0].attrib.get('y', 0)) + int(elements[0].attrib.get('height', 0)) // 2
                            d.click(center_x, center_y)
                            break

                # Если ничего не найдено, выходим из цикла
                if not found: break
                sleep(1)
        except: pass