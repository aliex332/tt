import os
import sys
import platform
import flet as ft
import webbrowser
import requests
from UI_INTERFACE.ResetFiles import ResetFiles
from cprint import cprint

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def RegisterModePage(page: ft.Page):
    if page.client_storage.get("Localisation") == 'EN':
        text1 = "This email service can be used for one-time registration confirmation on domains like Gmail, Outlook, Yahoo, and others. Using this service, you won't be able to recover your account after registration. It is suitable for one-time use only. Before start please check your balance!"
        text2 = "Using IMAP, you will be able to recover your accounts if necessary. It is recommended to use this action if you log into accounts frequently. Before starting, make sure you have enabled the IMAP protocol in your email settings. Also, configure a file with your emails. It should include the domain, port, login, and password. Each email will be linked to one account. If the file is empty, the script will stop working!"
        text3 = "Something went wrong! Please check your internet connection and your API Key. Make sure the kopeechka.store service is online and try again..."
        text4 = "Please check your IMAP file and make sure it is not empty. Also, verify the format of your emails. They should follow this format on each line: EMAIL:PASSWORD:DOMAIN:PORT\nAfter editing, please try again..."
        text6 = "Network settings will be reset before a new registration or if you get errors."
        text7 = "VPN will connect to selected countries. Configure .ovpn files in OpenVPN folder."
        text8 = "Proxy will connect to selected countries. Configure settings file in Proxy folder."
        text9 = "Mobile Network will be used instead of WiFi. Make sure your SIM card is working."
        text10 = "Before start, you need to configure your API or IMAP for email and specify the number of accounts."
        text11 = "You can select one or more regions to register. They will go in sequence."
        text12 = 'Selected:'


    if page.client_storage.get("Localisation") == 'RU':
        text1 = "Этот почтовый сервис можно использовать для одноразового подтверждения регистрации на таких доменах, как Gmail, Outlook, Yahoo и других. Вы не сможете восстановить свой аккаунт после регистрации. Перед началом проверьте ваш баланс!"
        text2 = "Используя IMAP, вы сможете восстановить свои аккаунты при необходимости. Рекомендуется для многоразового использования. Убедитесь, что протокол IMAP включен в настройках вашей почты. Настройте файл с вашими почтовыми адресами. Он должен содержать домен, порт, логин и пароль. Каждая почта будет связана с одним аккаунтом. Если файл пуст, скрипт прекратит работу!"
        text3 = "Что-то пошло не так! Пожалуйста, проверьте ваше подключение к интернету и ваш API-ключ. Убедитесь, что сервис kopeechka.store доступен, и попробуйте снова..."
        text4 = "Проверьте ваш IMAP-файл и убедитесь, что он не пуст. Также проверьте формат ваших почтовых адресов. Они должны соответствовать следующему формату в каждой строке: EMAIL:PASSWORD:DOMAIN:PORT\nПосле изменения, попробуйте ещё раз..."
        text6 = "Настройки сети будут сброшены перед новой регистрацией или в случае возникновения ошибок."
        text7 = "VPN будет подключаться к выбранным странам. Настройте .ovpn файлы в папке OpenVPN."
        text8 = "Прокси будет подключаться к выбранным странам. Настройте файл настроек в папке Proxy."
        text9 = "Мобильная сеть будет использоваться вместо WiFi. Убедитесь, что ваша SIM-карта работает."
        text10 = "Перед началом вам нужно настроить ваш API или IMAP для почты и указать количество аккаунтов."
        text11 = "Вы можете выбрать один или несколько регионов для регистрации. Они будут использоваться по порядку."
        text12 = 'Выбрано:'


    def UpdateStorage(switch_mobile_network=None, switch_reset_network=None, switch_use_proxy=None, switch_open_vpn=None, selected_countries=None, txt_number=None, country_iso2=None):
        iso2_codes = [country_iso2.get(country) for country in selected_countries if country in country_iso2]
        page.client_storage.set("mobile_network", switch_mobile_network.value)
        page.client_storage.set("reset_network", switch_reset_network.value)
        page.client_storage.set("proxy_enable", switch_use_proxy.value)
        page.client_storage.set("vpn_enable", switch_open_vpn.value)
        page.client_storage.set("accounts_count", int(txt_number.value))
        page.client_storage.set("country_code", list(iso2_codes))



        def handle_close(e):
            dlg_modal.open = False
            page.update()

        def Setup_IMAP(e):
            if platform.system() == "Windows": os.startfile(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase')

        def handle_segment_change(e, source):
            if e.control.selected_index == 0:  # Kopeechka
                api_key_input.visible = True
                get_api_button_container.visible = True
                space.width = 62
                setup_imap_button_container.visible = False
                actions_row.alignment = ft.MainAxisAlignment.SPACE_BETWEEN  # Разделяем кнопки
                result_text.value = text1
            elif e.control.selected_index == 1:  # IMAP
                api_key_input.visible = False
                get_api_button_container.visible = False
                space.width = 34
                setup_imap_button_container.visible = True
                actions_row.alignment = ft.MainAxisAlignment.END  # Выравниваем кнопки вправо
                result_text.value = text2
            page.update()

        def open_url(e):
            # Открытие ссылки в браузере
            webbrowser.open('https://kopeechka.store/?ref=26393', new=2)  # new=2 откроет в новом окне/вкладке

        def check_status(e):
            if segmented_button.selected_index == 0:
                api_key = api_key_input.value  # Получаем введенный API ключ
                url = f"https://api.kopeechka.store/user-balance?token={api_key}&cost=USD&type=json&api=2.0"

                try:
                    # Отправляем запрос к API
                    response = requests.get(url)
                    data = response.json()

                    # Обрабатываем ответ от API
                    if data["status"] == "OK":
                        balance = data["balance"]
                        if balance < 0.1:
                            result_text.value = f"Please top up your Kopeechka balance! Your balance is empty: {balance} USD."
                        else:
                            handle_close(e)
                            page.client_storage.set("register_mode", 'Kopeechka')
                            page.go("/UploadModePage")
                    else:
                        result_text.value = text3
                except Exception as e:
                    result_text.value = text3
                page.update()
                with open(f'{local_path}/resource/Kopeechka.txt', 'w') as f:
                    f.write(api_key)

            if segmented_button.selected_index == 1:
                with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/IMAP.txt', 'r') as file:
                    lines = file.readlines()

                    for line in lines:
                        line = line.strip()

                        parts = line.split(":")
                        if len(parts) == 4:
                            email, password, domain, port = parts
                            if port.isdigit():
                                handle_close(e)
                                page.client_storage.set("register_mode", 'IMAP')
                                page.go("/UploadModePage")
                                return True

                result_text.value = text4
                page.update()
                return False

        result_text = ft.Text(value=text1)  # Default text

        segmented_button = ft.CupertinoSegmentedButton(
            selected_index=0,
            border_color='#191919',
            click_color='black',
            unselected_color='black',
            selected_color='#27ae60',
            on_change=lambda e: handle_segment_change(e, source='buttons'),
            controls=[
                ft.Container(
                    padding=ft.padding.symmetric(0, 30),
                    content=ft.Text("Kopeechka", color='white'),
                ),
                ft.Container(
                    padding=ft.padding.symmetric(0, 30),
                    content=ft.Text("IMAP", color='white'),
                ),
            ]
        )

        try:
            with open(f'{local_path}/resource/Kopeechka.txt', 'r') as f:
                file_content = f.read().strip()  # Считываем содержимое файла
        except FileNotFoundError:
            file_content = ''

        value = file_content if file_content else 'Paste your API key here:'

        api_key_input = ft.TextField(
            label="API Key:",
            value=value,
            text_align="center",
            border_radius=0,
            text_style=ft.TextStyle(size=13, color='WHITE70'),
            border_color='grey',
            visible=True,
            on_focus=lambda e: (setattr(api_key_input, 'value', ''), page.update()) if api_key_input.value == value else None,
            on_blur=lambda e: (setattr(api_key_input, 'value', value), page.update()) if not api_key_input.value else None
        )

        # Контейнер для кнопки Get API
        get_api_button_container = ft.Container(
            content=ft.TextButton("Get API", on_click=open_url, style=ft.ButtonStyle(color='green')),
            visible=True
        )

        setup_imap_button_container = ft.Container(
            content=ft.TextButton("Setup IMAP", on_click=Setup_IMAP, style=ft.ButtonStyle(color='green')),
            visible=False
        )

        space = ft.Container(width=62)

        # Row для кнопок
        actions_row = ft.Row(
            controls=[
                get_api_button_container,  # Оборачиваем кнопку в контейнер
                setup_imap_button_container,
                space,
                ft.TextButton("Submit", on_click=check_status),
                ft.TextButton("Cancel", on_click=handle_close),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Разделяем кнопки по умолчанию
        )

        dlg_modal = ft.AlertDialog(
            modal=True,
            barrier_color=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            bgcolor='#1c1c1e',
            inset_padding=ft.padding.all(0),
            content=ft.Container(
                width=292,
                height=230,
                content=ft.Column(
                    controls=[segmented_button, api_key_input, result_text],
                    spacing=15
                )
            ),
            actions=[actions_row],  # Добавляем Row с кнопками
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()

    def OpenFolder():
        if platform.system() == "Windows": os.startfile(f'{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/{last_active_switch["folder_path"]}/')
        if platform.system() == "Darwin": os.system(f'open {local_path}/iPhoneTikTokFiles/iPhoneNetSettings/{last_active_switch["folder_path"]}/')

    def RecoverFolder():
        ResetFiles(last_active_switch["folder_path"])

    page.window.width = 1024
    page.window.height = 650
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = True
    page.window.full_screen = False

    page.fonts = {
        "TikTok Bold": "fonts/TikTokText-Bold.ttf",
        "TikTok Medium": "fonts/TikTokText-Medium.ttf",
        "TikTok Regular": "fonts/TikTokText-Regular.ttf",
    }

    next_button = ft.ElevatedButton(
        text="NEXT",  # Текст кнопки
        on_click=lambda e: UpdateStorage(
            switch_mobile_network,
            switch_reset_network,
            switch_use_proxy,
            switch_open_vpn,
            selected_countries,
            txt_number,
            country_iso2
        ),
        color="white",  # Цвет текста
        bgcolor="grey",  # Изначально серый фон
        disabled=True,  # Кнопка неактивна
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),  # Закругленные углы
        ),
    )

    def open_url_info(e):
        if page.client_storage.get("Localisation") == 'EN': webbrowser.open('https://google.com', new=2)  # new=2 откроет в новом окне/вкладке
        if page.client_storage.get("Localisation") == 'RU': webbrowser.open('https://google.com', new=2)  # new=2 откроет в новом окне/вкладке

    info_button = ft.IconButton(
                    icon=ft.Icons.INFO_OUTLINE_ROUNDED,  # Иконка
                    icon_size=20,
                    tooltip="More information",
                    on_click=lambda e: open_url_info(e),  # Обработчик клика
                    icon_color="white",  # Цвет иконки
                    visible=True
                )

    # Создаем AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("SETUP REGISTER MODE", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,  # Отключаем эффект повышения при скролле
        leading=ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=lambda e: page.go("/MainMenuPage")),
        actions=[  # Добавляем кнопку в правую часть AppBar
            ft.Container(
                content=info_button
            ),
            ft.Container(
                content=next_button,
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
        ]
    )

    # Иконки
    proxy_icon = ft.Icon(ft.Icons.NETWORK_CHECK_SHARP, size=22)
    mobile_network_icon = ft.Icon(ft.Icons.NETWORK_CELL, size=22, color=ft.Colors.YELLOW)
    vpn_icon = ft.Icon(ft.Icons.LOCK, size=22, color=ft.Colors.GREEN)
    reset_icon = ft.Icon(ft.Icons.UPDATE, size=22, color=ft.Colors.RED)

    # Переключатели
    switch_reset_network = ft.Switch(value=False, label="Reset Network ", label_position=ft.LabelPosition.LEFT, thumb_color=ft.Colors.WHITE, track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY}, focus_color=ft.Colors.PURPLE, label_style=ft.TextStyle(size=18, font_family="TikTok Bold"), on_change=lambda e: update_content("reset_network"))
    switch_open_vpn = ft.Switch(value=False, label="Use OpenVPN ", label_position=ft.LabelPosition.LEFT, thumb_color=ft.Colors.WHITE, track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY}, focus_color=ft.Colors.PURPLE, label_style=ft.TextStyle(size=18, font_family="TikTok Bold"), on_change=lambda e: handle_switch_change("vpn_enable"))
    switch_use_proxy = ft.Switch(value=False, label="Use Proxy ", label_position=ft.LabelPosition.LEFT, thumb_color=ft.Colors.WHITE, track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY}, focus_color=ft.Colors.PURPLE, label_style=ft.TextStyle(size=18, font_family="TikTok Bold"), on_change=lambda e: handle_switch_change("proxy_enable"))
    switch_mobile_network = ft.Switch(value=False, label="Mobile Network ", label_position=ft.LabelPosition.LEFT, thumb_color=ft.Colors.WHITE, track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY}, focus_color=ft.Colors.PURPLE, label_style=ft.TextStyle(size=18, font_family="TikTok Bold"), on_change=lambda e: handle_switch_change("mobile_network"))

    # Функция для обновления текста и картинки
    image = ft.Image(src=f"{local_path}/resource/assets/photo/Signup.png", left=130, top=-130) # Изначальная картинка
    last_active_switch = {"name": None} # Последний активный переключатель
    def update_content(changed_switch=None):
        if changed_switch == "reset_network" and switch_reset_network.value:
            text_content.value = text6
            image.src = f"{local_path}/resource/assets/photo/Reset.png"
            last_active_switch["name"] = "reset_network"
            folder_button.visible = False
            recover_button.visible = False
        elif changed_switch == "vpn_enable" and switch_open_vpn.value:
            text_content.value = text7
            image.src = f"{local_path}/resource/assets/photo/VPN.png"
            last_active_switch["name"] = "vpn_enable"
            last_active_switch["folder_path"] = "VPN"
            folder_button.visible = True
            recover_button.visible = True
        elif changed_switch == "proxy_enable" and switch_use_proxy.value:
            text_content.value = text8
            image.src = f"{local_path}/resource/assets/photo/Proxy.png"
            last_active_switch["name"] = "proxy_enable"
            last_active_switch["folder_path"] = "Proxy"
            folder_button.visible = True
            recover_button.visible = True
        elif changed_switch == "mobile_network" and switch_mobile_network.value:
            text_content.value = text9
            image.src = f"{local_path}/resource/assets/photo/MobileNetwork.png"
            last_active_switch["name"] = "mobile_network"
        elif not switch_reset_network.value and not switch_open_vpn.value and not switch_use_proxy.value and not switch_mobile_network.value:
            text_content.value = text10
            image.src = f"{local_path}/resource/assets/photo/Signup.png"
            last_active_switch["name"] = None
            folder_button.visible = False
            recover_button.visible = False
        page.update()

    # Функция для управления конфликтующими переключателями
    def handle_switch_change(changed_switch):
        if changed_switch == "vpn_enable" and switch_open_vpn.value: switch_use_proxy.value = False
        elif changed_switch == "proxy_enable" and switch_use_proxy.value: switch_open_vpn.value = False; switch_mobile_network.value = False
        elif changed_switch == "mobile_network" and switch_mobile_network.value: switch_use_proxy.value = False
        update_content(changed_switch)

    all_countries = ["Australia", "Austria", "Canada", "United Kingdom", "United States", "Germany", "Sweden", "Belgium", "Netherlands", "Norway", "Spain", "Switzerland", "Denmark", "New Zealand", "Finland", "France", "Italy", "Ireland", "Iceland", "Cyprus", "Czech Republic", "Greece", "Lithuania", "Estonia", "Latvia", "Poland", "Slovakia", "Slovenia", "Portugal", "Hungary", "Romania", "Israel", "South Africa", "Singapore", "Japan", "Ukraine", "Afghanistan", "Albania", "Algeria", "Andorra",
                     "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Djibouti", "Dominica",
                     "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Eswatini (fmr. Swaziland)", "Ethiopia", "Fiji", "Gabon", "Gambia", "Georgia", "Ghana", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "India", "Indonesia", "Iran", "Iraq", "Jamaica", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea (North)", "Korea (South)", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Lesotho", "Liberia", "Libya",
                     "Liechtenstein", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal", "Nicaragua", "Niger", "Nigeria", "North Macedonia (formerly Macedonia)", "Oman", "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru",
                     "Philippines", "Qatar", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Solomon Islands", "Somalia", "South Sudan", "Sri Lanka", "Sudan", "Suriname", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
                     "United Arab Emirates", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

    country_iso2 = {
        "Australia": "AU",
        "Austria": "AT",
        "Canada": "CA",
        "United Kingdom": "GB",
        "United States": "US",
        "Germany": "DE",
        "Sweden": "SE",
        "Belgium": "BE",
        "Netherlands": "NL",
        "Norway": "NO",
        "Spain": "ES",
        "Switzerland": "CH",
        "Denmark": "DK",
        "New Zealand": "NZ",
        "Finland": "FI",
        "France": "FR",
        "Italy": "IT",
        "Ireland": "IE",
        "Iceland": "IS",
        "Cyprus": "CY",
        "Czech Republic": "CZ",
        "Greece": "GR",
        "Lithuania": "LT",
        "Estonia": "EE",
        "Latvia": "LV",
        "Poland": "PL",
        "Slovakia": "SK",
        "Slovenia": "SI",
        "Portugal": "PT",
        "Hungary": "HU",
        "Romania": "RO",
        "Israel": "IL",
        "South Africa": "ZA",
        "Singapore": "SG",
        "Japan": "JP",
        "Ukraine": "UA",
        "Afghanistan": "AF",
        "Albania": "AL",
        "Algeria": "DZ",
        "Andorra": "AD",
        "Angola": "AO",
        "Antigua and Barbuda": "AG",
        "Argentina": "AR",
        "Armenia": "AM",
        "Azerbaijan": "AZ",
        "Bahamas": "BS",
        "Bahrain": "BH",
        "Bangladesh": "BD",
        "Barbados": "BB",
        "Belarus": "BY",
        "Belize": "BZ",
        "Benin": "BJ",
        "Bhutan": "BT",
        "Bolivia": "BO",
        "Bosnia and Herzegovina": "BA",
        "Botswana": "BW",
        "Brazil": "BR",
        "Brunei": "BN",
        "Bulgaria": "BG",
        "Burkina Faso": "BF",
        "Burundi": "BI",
        "Cabo Verde": "CV",
        "Cambodia": "KH",
        "Cameroon": "CM",
        "Central African Republic": "CF",
        "Chad": "TD",
        "Chile": "CL",
        "China": "CN",
        "Colombia": "CO",
        "Comoros": "KM",
        "Congo (Congo-Brazzaville)": "CG",
        "Costa Rica": "CR",
        "Croatia": "HR",
        "Cuba": "CU",
        "Djibouti": "DJ",
        "Dominica": "DM",
        "Dominican Republic": "DO",
        "Ecuador": "EC",
        "Egypt": "EG",
        "El Salvador": "SV",
        "Equatorial Guinea": "GQ",
        "Eritrea": "ER",
        "Eswatini (fmr. Swaziland)": "SZ",
        "Ethiopia": "ET",
        "Fiji": "FJ",
        "Gabon": "GA",
        "Gambia": "GM",
        "Georgia": "GE",
        "Ghana": "GH",
        "Grenada": "GD",
        "Guatemala": "GT",
        "Guinea": "GN",
        "Guinea-Bissau": "GW",
        "Guyana": "GY",
        "Haiti": "HT",
        "Holy See": "VA",
        "Honduras": "HN",
        "India": "IN",
        "Indonesia": "ID",
        "Iran": "IR",
        "Iraq": "IQ",
        "Jamaica": "JM",
        "Jordan": "JO",
        "Kazakhstan": "KZ",
        "Kenya": "KE",
        "Kiribati": "KI",
        "Korea (North)": "KP",
        "Korea (South)": "KR",
        "Kuwait": "KW",
        "Kyrgyzstan": "KG",
        "Laos": "LA",
        "Lebanon": "LB",
        "Lesotho": "LS",
        "Liberia": "LR",
        "Libya": "LY",
        "Liechtenstein": "LI",
        "Luxembourg": "LU",
        "Madagascar": "MG",
        "Malawi": "MW",
        "Malaysia": "MY",
        "Maldives": "MV",
        "Mali": "ML",
        "Malta": "MT",
        "Marshall Islands": "MH",
        "Mauritania": "MR",
        "Mauritius": "MU",
        "Mexico": "MX",
        "Micronesia": "FM",
        "Moldova": "MD",
        "Monaco": "MC",
        "Mongolia": "MN",
        "Montenegro": "ME",
        "Morocco": "MA",
        "Mozambique": "MZ",
        "Myanmar (formerly Burma)": "MM",
        "Namibia": "NA",
        "Nauru": "NR",
        "Nepal": "NP",
        "Nicaragua": "NI",
        "Niger": "NE",
        "Nigeria": "NG",
        "North Macedonia (formerly Macedonia)": "MK",
        "Oman": "OM",
        "Pakistan": "PK",
        "Palau": "PW",
        "Palestine State": "PS",
        "Panama": "PA",
        "Papua New Guinea": "PG",
        "Paraguay": "PY",
        "Peru": "PE",
        "Philippines": "PH",
        "Qatar": "QA",
        "Russia": "RU",
        "Rwanda": "RW",
        "Saint Kitts and Nevis": "KN",
        "Saint Lucia": "LC",
        "Saint Vincent and the Grenadines": "VC",
        "Samoa": "WS",
        "San Marino": "SM",
        "Sao Tome and Principe": "ST",
        "Saudi Arabia": "SA",
        "Senegal": "SN",
        "Serbia": "RS",
        "Seychelles": "SC",
        "Sierra Leone": "SL",
        "Solomon Islands": "SB",
        "Somalia": "SO",
        "South Sudan": "SS",
        "Sri Lanka": "LK",
        "Sudan": "SD",
        "Suriname": "SR",
        "Syria": "SY",
        "Tajikistan": "TJ",
        "Tanzania": "TZ",
        "Thailand": "TH",
        "Timor-Leste": "TL",
        "Togo": "TG",
        "Tonga": "TO",
        "Trinidad and Tobago": "TT",
        "Tunisia": "TN",
        "Turkey": "TR",
        "Turkmenistan": "TM",
        "Tuvalu": "TV",
        "Uganda": "UG",
        "United Arab Emirates": "AE",
        "Uruguay": "UY",
        "Uzbekistan": "UZ",
        "Vanuatu": "VU",
        "Venezuela": "VE",
        "Vietnam": "VN",
        "Yemen": "YE",
        "Zambia": "ZM",
        "Zimbabwe": "ZW"
    }

    # Текст для отображения выбранных стран
    selected_text = ft.Text(f"{text12} ", width=300, font_family="TikTok Regular")

    # Функция для обновления чекбоксов
    filtered_countries = all_countries.copy() # Для отслеживания текущих фильтрованных стран
    checkbox_column = ft.Column(scroll=ft.ScrollMode.AUTO)
    def update_checkboxes():
        checkbox_column.controls.clear()
        for country in filtered_countries:
            checkbox = ft.Checkbox(
                label=country,
                value=country in selected_countries,
                on_change=update_selected,
            )
            checkbox_column.controls.append(checkbox)
        page.update()

    # Обновление списка выбранных стран
    selected_countries = set()

    def enable_next_button():
        if selected_countries:
            next_button.bgcolor = "red"
            next_button.disabled = False  # Кнопка активна
        else:
            next_button.bgcolor = "grey"
            next_button.disabled = True  # Кнопка неактивна

        if txt_number.value == 'Accounts' or txt_number.value == 0:
            next_button.bgcolor = "grey"
            next_button.disabled = True  # Кнопка неактивна

    def update_selected(e):
        if e.control.value:
            selected_countries.add(e.control.label)
        else:
            selected_countries.discard(e.control.label)

        # Создаем строку с выбранными странами
        selected_countries_text = ', '.join(selected_countries)

        # Проверяем ширину текста и ограничиваем, если превышает 300px
        if selected_text.width:
            max_width = selected_text.width
            current_text_length = len(selected_countries_text) * 15

            # Если текст слишком длинный
            if current_text_length > max_width:
                selected_countries_list = list(selected_countries)[:2]  # Оставляем только 3 страны
                selected_countries_list.append("...")  # Добавляем многоточие
                selected_countries_text = ', '.join(selected_countries_list)  # Формируем строку с многоточием
            else:
                selected_countries_text = ', '.join(selected_countries)  # Если текст вмещается, показываем все страны

        # Обновляем текст на экране
        selected_text.value = f"{text12} {selected_countries_text}"

        enable_next_button()
        page.update()

    # Функция для показа/скрытия нижнего меню
    dropdown_content = ft.Column(
        controls=[],
        visible=False,
        width=300,
        height=175,
        scroll=ft.ScrollMode.AUTO,
    )

    arrow_icon = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN)

    dropdown_open = False # Флаг для отслеживания состояния выпадающего списка
    def toggle_dropdown(e=None):
        nonlocal dropdown_open
        dropdown_open = not dropdown_open
        dropdown_content.visible = dropdown_open
        arrow_icon.name = ft.Icons.KEYBOARD_ARROW_UP if dropdown_open else ft.Icons.KEYBOARD_ARROW_DOWN
        update_checkboxes()
        if dropdown_open: text_content.value = text11
        else: text_content.value = text10
        folder_button.visible = False
        recover_button.visible = False
        page.update()

    # Кнопка для открытия/закрытия списка
    search_field = ft.Container(
        content=ft.Row(
            [
                ft.Text("Choose country:", expand=True, font_family="TikTok Regular", color='WHITE70'),
                arrow_icon,  # Иконка стрелки
            ],
        ),
        width=300,  # Устанавливаем ширину кнопки
        on_click=toggle_dropdown,  # Обработка клика
        border=ft.border.all(1, ft.Colors.WHITE),  # Белая обводка
        border_radius=0,
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.TRANSPARENT,  # Прозрачный фон (можно поменять при необходимости)
    )

    # Инициализация интерфейса
    update_checkboxes()
    dropdown_content.controls.append(checkbox_column)

    txt_number = ft.TextField(label="Accounts:", value=0, text_align="center", border_radius=0, text_style=ft.TextStyle(font_family="TikTok Bold", size=13, color='WHITE70'),
        width=100,  # Устанавливаем ширину
        height=45,
        border_color='white'
    )

    def validate_number(value):
        enable_next_button()
        return max(int(value), 1) if isinstance(value, str) and value.isdigit() else 0

    def minus_click(e):
        txt_number.value = validate_number(txt_number.value)
        txt_number.value = str(max(int(txt_number.value) - 1, 1))  # Минимальное значение - 1
        enable_next_button()
        page.update()

    def plus_click(e):
        txt_number.value = validate_number(txt_number.value)
        txt_number.value = str(int(txt_number.value) + 1)
        enable_next_button()
        page.update()

    def on_change(e):
        txt_number.value = validate_number(txt_number.value)
        enable_next_button()
        page.update()

    txt_number.on_change = on_change


    text_content = ft.Text(
        value=text10,
        size=15,
        font_family="TikTok Regular",
        width=300,
    )

    folder_button = ft.IconButton(
        icon=ft.Icons.FOLDER_COPY_OUTLINED,  # Иконка
        icon_size=30,
        tooltip="Open settings",
        on_click=lambda e: OpenFolder(),  # Обработчик клика
        icon_color="white",  # Цвет иконки
        visible=False
    )

    recover_button = ft.IconButton(
        icon=ft.Icons.AUTO_DELETE_OUTLINED,  # Иконка
        icon_size=30,
        tooltip="Reset settings",
        on_click=lambda e: RecoverFolder(),  # Обработчик клика
        icon_color="white",  # Цвет иконки
        visible=False
    )

    right_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=text_content,  # Текстовый элемент
                    padding=ft.padding.only(bottom=0),  # Отступ снизу
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            search_field,  # Поле поиска
                            dropdown_content,  # Контейнер с выпадающим списком
                            selected_text,  # Текст для отображения выбранных стран
                        ],
                    ),
                    padding=ft.padding.only(top=10),  # Отступ сверху
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            txt_number,
                            ft.IconButton(icon=ft.Icons.REMOVE, on_click=minus_click),
                            ft.IconButton(icon=ft.Icons.ADD, on_click=plus_click),
                            folder_button,
                            recover_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(top=10, bottom=20),  # Отступы сверху и снизу
                ),
            ],
            spacing=10,  # Общий отступ между элементами в колонке
        ),
        left=650,
        top=80,
    )


    stack = ft.Stack(
        controls=[
            image,
            right_container,
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[mobile_network_icon, switch_mobile_network],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[reset_icon, switch_reset_network],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[vpn_icon, switch_open_vpn],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[proxy_icon, switch_use_proxy],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                left=50,
                top=80,
            ),
        ]
    )
    page.add(stack)
