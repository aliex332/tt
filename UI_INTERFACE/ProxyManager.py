import os
import sys
import platform
import flet as ft

def ProxyManager(page: ft.Page):
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
        "Czech Rep.": "CZ",
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
        "Antigua & Barb.": "AG",
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
        "Bosnia & Herz.": "BA",
        "Botswana": "BW",
        "Brazil": "BR",
        "Brunei": "BN",
        "Bulgaria": "BG",
        "Burkina Faso": "BF",
        "Burundi": "BI",
        "Cabo Verde": "CV",
        "Cambodia": "KH",
        "Cameroon": "CM",
        "CAR": "CF",
        "Chad": "TD",
        "Chile": "CL",
        "China": "CN",
        "Colombia": "CO",
        "Comoros": "KM",
        "Congo": "CG",
        "Costa Rica": "CR",
        "Croatia": "HR",
        "Cuba": "CU",
        "Djibouti": "DJ",
        "Dominica": "DM",
        "Dom. Rep.": "DO",
        "Ecuador": "EC",
        "Egypt": "EG",
        "El Salvador": "SV",
        "Eq. Guinea": "GQ",
        "Eritrea": "ER",
        "Eswatini": "SZ",
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
        "N. Korea": "KP",
        "S. Korea": "KR",
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
        "Marshall Is.": "MH",
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
        "Myanmar": "MM",
        "Namibia": "NA",
        "Nauru": "NR",
        "Nepal": "NP",
        "Nicaragua": "NI",
        "Niger": "NE",
        "Nigeria": "NG",
        "N. Macedonia": "MK",
        "Oman": "OM",
        "Pakistan": "PK",
        "Palau": "PW",
        "Palestine": "PS",
        "Panama": "PA",
        "Papua N.G.": "PG",
        "Paraguay": "PY",
        "Peru": "PE",
        "Philippines": "PH",
        "Qatar": "QA",
        "Russia": "RU",
        "Rwanda": "RW",
        "St. Kitts & Nevis": "KN",
        "St. Lucia": "LC",
        "St. Vincent & Gren.": "VC",
        "Samoa": "WS",
        "San Marino": "SM",
        "Sao Tome & Prin.": "ST",
        "Saudi Arabia": "SA",
        "Senegal": "SN",
        "Serbia": "RS",
        "Seychelles": "SC",
        "Sierra Leone": "SL",
        "Solomon Is.": "SB",
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
        "Trinidad & Tobago": "TT",
        "Tunisia": "TN",
        "Turkey": "TR",
        "Turkmenistan": "TM",
        "Tuvalu": "TV",
        "Uganda": "UG",
        "UAE": "AE",
        "Uruguay": "UY",
        "Uzbekistan": "UZ",
        "Vanuatu": "VU",
        "Venezuela": "VE",
        "Vietnam": "VN",
        "Yemen": "YE",
        "Zambia": "ZM",
        "Zimbabwe": "ZW"
    }
    all_countries = [
        "Australia", "Austria", "Canada", "United Kingdom", "United States", "Germany", "Sweden", "Belgium",
        "Netherlands", "Norway", "Spain", "Switzerland", "Denmark", "New Zealand", "Finland", "France",
        "Italy", "Ireland", "Iceland", "Cyprus", "Czech Rep.", "Greece", "Lithuania", "Liechtenstein", "Luxembourg", "Estonia", "Latvia",
        "Poland", "Slovakia", "Slovenia", "Portugal", "Hungary", "Romania", "Israel", "South Africa",
        "Singapore", "Japan", "Ukraine", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
        "Antigua & Barb.", "Argentina", "Armenia", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
        "Barbados", "Belarus", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia & Herz.", "Botswana",
        "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon",
        "CAR", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba",
        "Djibouti", "Dominica", "Dom. Rep.", "Ecuador", "Egypt", "El Salvador", "Eq. Guinea", "Eritrea",
        "Eswatini", "Ethiopia", "Fiji", "Gabon", "Gambia", "Georgia", "Ghana", "Grenada", "Guatemala",
        "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "India", "Indonesia", "Iran",
        "Iraq", "Jamaica", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "N. Korea", "S. Korea", "Kuwait",
        "Kyrgyzstan", "Laos", "Lebanon", "Lesotho", "Liberia", "Libya",
        "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Is.", "Mauritania",
        "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
        "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Nicaragua", "Niger", "Nigeria",
        "N. Macedonia", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua N.G.", "Paraguay",
        "Peru", "Philippines", "Qatar", "Russia", "Rwanda", "St. Kitts & Nevis", "St. Lucia",
        "St. Vincent & Gren.", "Samoa", "San Marino", "Sao Tome & Prin.", "Saudi Arabia", "Senegal",
        "Serbia", "Seychelles", "Sierra Leone", "Solomon Is.", "Somalia", "South Sudan", "Sri Lanka",
        "Sudan", "Suriname", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga",
        "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "UAE", "Uruguay",
        "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]

    if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
    else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    def OpenFolder(folder_path):
        if platform.system() == "Windows": os.startfile(f'{local_path}/iPhoneTikTokFiles/{folder_path}')
        if platform.system() == "Darwin": os.system(f'open {local_path}/iPhoneTikTokFiles/{folder_path}')

    def CloseButton():
        if page.client_storage.get("Register") is True: page.go('/RegisterModePage')
        elif page.client_storage.get("Login") is True: page.go('/LoginModePage')
        else: page.go('/MainMenuPage')

    page.window.width = 1024
    page.window.height = 660
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = True
    page.window.full_screen = False
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#191919"

    page.fonts = {
        "TikTok Bold": "fonts/TikTokText-Bold.ttf",
        "TikTok Medium": "fonts/TikTokText-Medium.ttf",
        "TikTok Regular": "fonts/TikTokText-Regular.ttf",
    }

    page.appbar = ft.AppBar(
        title=ft.Text("PROXY MANAGER", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,
        leading=ft.IconButton(ft.Icons.CLOSE, on_click=lambda e: CloseButton()),
        actions=[
            ft.Container(
                content=ft.IconButton(ft.Icons.VPN_LOCK_OUTLINED, on_click=lambda e: page.go('/VpnManager'), icon_size=20, tooltip='VPN Manager'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(ft.Icons.MARK_EMAIL_UNREAD_OUTLINED, on_click=lambda e: page.go('/ImapManager'), tooltip='IMAP list'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(ft.Icons.SWITCH_ACCOUNT_OUTLINED, on_click=lambda e: page.go('/AccountManager'), tooltip='Accounts Manager'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(icon=ft.Icons.FOLDER_COPY_OUTLINED, icon_size=24, tooltip="PROXY Folder", on_click=lambda e: OpenFolder('iPhoneNetSettings/Proxy'), icon_color="blue"),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
        ]
    )


    proxy_number = ft.IconButton(
        icon=ft.Icons.FILTER_LIST_OUTLINED,
        icon_color="white",
        disabled=True
    )

    dropdown_options = [ft.dropdown.Option(country) for country in all_countries]

    country_dropdown = ft.Dropdown(
        width=170,
        hint_content=ft.Row(
            [
                ft.Icon(ft.Icons.LANGUAGE, color="white"),
                ft.Text('Country', text_align=ft.TextAlign.CENTER, color="white", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        border_color="white",
        text_size=15,
        options=dropdown_options,
        on_change=lambda e: update_save_button_state()
    )

    def update_save_button_state():
        if ip_field.value and port_field.value and login_field.value and password_field.value and country_dropdown.value: save_button.disabled = False; save_button.icon_color = '#1dd1a1'  # Активируем кнопку
        else: save_button.disabled = True; save_button.icon_color = 'white'
        page.update()  # Обновляем интерфейс

    def save_button_clicked(e):
        country_code = country_iso2.get(country_dropdown.value)
        proxy_data = f'{country_code}:{ip_field.value}:{port_field.value}:{login_field.value}:{password_field.value}'.rstrip(':')
        with open(f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/Proxy/Proxy.txt", "r+") as file:
            existing_data = [line.strip() for line in file if line.strip()]  # Чистим пробелы и пустые строки
            file.seek(0)  # Возвращаемся в начало файла
            file.write(f"{proxy_data}\n")  # Добавляем новую строку
            file.writelines(f"{line}\n" for line in existing_data)  # Перезаписываем остальные строки
            file.truncate()  # Удаляем лишние данные, если файл стал короче
        update_ui(scrollable_container)
        country_dropdown.value = ''
        ip_field.value = ''
        port_field.value = ''
        login_field.value = ''
        password_field.value = ''
        save_button.icon_color = 'white'
        save_button.disabled = True
        page.update()


    ip_field = ft.TextField(
        label=ft.Text("IP", color='white', font_family="TikTok Regular", size=15),
        width=150,
        border_color='white',
        prefix_icon=ft.Icon(ft.Icons.PRIVACY_TIP_OUTLINED, color="white"),
        on_change=lambda e: update_save_button_state()
    )

    port_field = ft.TextField(
        label=ft.Text("Port", color='white', font_family="TikTok Regular", size=15),
        width=150,
        border_color='white',
        prefix_icon=ft.Icon(ft.Icons.WIFI_TETHERING, color="white"),
        password=False,
        on_change=lambda e: update_save_button_state()
    )

    login_field = ft.TextField(
        label=ft.Text("Login", color='white', font_family="TikTok Regular", size=15),
        width=150,
        border_color='white',
        prefix_icon=ft.Icon(ft.Icons.PERSON, color="white"),
        on_change=lambda e: update_save_button_state()
    )

    password_field = ft.TextField(
        label=ft.Text("Password", color='white', font_family="TikTok Regular", size=15),
        width=150,
        border_color='white',
        prefix_icon=ft.Icon(ft.Icons.LOCK_PERSON_OUTLINED, color="white"),
        password=False,
        on_change=lambda e: update_save_button_state()
    )

    # Создаем кнопку Save
    save_button = ft.IconButton(
        icon=ft.Icons.CHECKLIST,
        icon_color="white",
        icon_size=25,
        tooltip="Save",
        on_click=save_button_clicked,  # Привязываем обработчик
        disabled=True
    )

    row_content = ft.Row(
        [
            proxy_number,
            country_dropdown,
            ip_field,
            port_field,
            login_field,
            password_field,
            save_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )

    bottom_app_bar = ft.BottomAppBar(
        content=row_content,
        bgcolor="#4b4b4b",
        height=70,
    )


    def GetProxyBase():
        with open(f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/Proxy/Proxy.txt") as f:  ## Открываем файл
            lines = [line.strip() for line in f]
            return lines

    def GetProxyFromBase(proxy_data):
        proxy_data = proxy_data.split(':')
        return proxy_data[0], proxy_data[1], proxy_data[2], proxy_data[3], proxy_data[4]

    def delete_account(delete_data, scrollable_container):
        delete_data = delete_data.replace(':None', '').strip()  # Удаляем ':None' и обрезаем пробелы

        # Читаем все аккаунты из файла
        proxy = GetProxyBase()

        # Удаляем строку с нужным аккаунтом (сравнение по обрезанным строкам)
        updated_accounts = [account.strip() for account in proxy if account.strip() != delete_data]

        # Перезаписываем файл без удаленной строки
        with open(f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/Proxy/Proxy.txt", 'w') as f:
            for account in updated_accounts: f.write(f"{account}\n")

        # Обновляем UI с уже обновленными данными
        update_ui(scrollable_container)

    def create_empty_message():
        """Создаёт контейнер с сообщением о пустом списке."""
        return ft.Container(
            content=ft.Text(
                "Your proxy list is empty!\nAdd your proxy here before using...",
                size=18,
                color="#b2bec3",
                text_align=ft.TextAlign.CENTER,
                font_family="TikTok Regular",
            ),
            alignment=ft.alignment.center,
            expand=True,
            margin=ft.Margin(top=200, left=0, right=0, bottom=0)
        )

    def update_ui(scrollable_container):
        """Обновляет интерфейс с учётом обновлённого списка аккаунтов."""
        updated_proxy = GetProxyBase()

        # Создаем строки ввода для каждого аккаунта
        input_rows = [create_input_row(i, account) for i, account in enumerate(updated_proxy)]

        # Проверяем, пустой ли список
        if not input_rows:
            # Если список пуст, показываем сообщение
            if isinstance(scrollable_container, ft.Container):
                scrollable_container.content = create_empty_message()
            else:
                scrollable_container.controls.clear()
                scrollable_container.controls.append(create_empty_message())
        else:
            # Если список не пуст, обновляем данные
            if isinstance(scrollable_container, ft.Container):
                scrollable_container.content = ft.Column(input_rows, spacing=5, expand=True)
            else:
                scrollable_container.controls.clear()
                scrollable_container.controls.extend(input_rows)

        # Обновляем страницу
        page.update()


    def create_input_row(index, proxy_data):
        country_code, proxy_ip, proxy_port, proxy_login, proxy_password = GetProxyFromBase(proxy_data)
        delete_data = f'{country_code}:{proxy_ip}:{proxy_port}:{proxy_login}:{proxy_password}'
        country_name = next((name for name, iso2 in country_iso2.items() if iso2 == country_code), None)

        proxy_number = ft.Text(
            f"{index + 1}",
            color="#dfe6e9",
            size=16,
            weight=ft.FontWeight.BOLD,
            width=30,
            text_align=ft.TextAlign.CENTER,
            font_family="TikTok Bold"
        )

        country_dropdown_value = country_name

        country_dropdown = ft.Dropdown(
            width=150,
            hint_content=ft.Row(
                [
                    ft.Text(country_dropdown_value, text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            border_color="#636e72",
            text_size=15,
            value=country_dropdown_value,
        )

        ip_field = ft.TextField(
            label=ft.Text('IP', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            value=proxy_ip,
            text_style=ft.TextStyle(color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            read_only=True
        )

        port_field = ft.TextField(
            label=ft.Text('IP', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            value=proxy_port,
            text_style=ft.TextStyle(color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            read_only=True
        )

        login_field = ft.TextField(
            label=ft.Text('Login', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            prefix_icon=ft.Icon(ft.Icons.PERSON, color="#b2bec3", visible=False),
            value=proxy_login,
            text_style=ft.TextStyle(color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            read_only=True
        )

        password_field = ft.TextField(
            label=ft.Text('Password', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            prefix_icon=ft.Icon(ft.Icons.LOCK, color="#b2bec3", visible=False),
            value=proxy_password,
            text_style=ft.TextStyle(color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            read_only=True,
        )

        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
            icon_color="red",
            tooltip="Delete",
            on_click=lambda e: delete_account(delete_data, scrollable_container),
            visible=True
        )

        row_content = ft.Row(
            [
                proxy_number,
                country_dropdown,
                ip_field,
                port_field,
                login_field,
                password_field,
                delete_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        )

        return ft.Container(
            content=row_content,
            bgcolor="#2C2C2C",
            padding=7,
            border_radius=5,
            border=ft.border.all(1, "black"),
        )

    # Получаем все аккаунты из базы
    proxy = GetProxyBase()

    # Создаем строки ввода для каждого аккаунта
    input_rows = [create_input_row(i, account) for i, account in enumerate(proxy)]
    if not input_rows:
        scrollable_container = ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Your proxy list is empty!\nAdd your proxy here before using...",
                        size=18,
                        color="#b2bec3",
                        text_align=ft.TextAlign.CENTER,
                        font_family="TikTok Regular"
                    ),
                    alignment=ft.alignment.center,  # Центруем текст внутри контейнера
                    expand=True,
                    margin=ft.Margin(top=200, left=0, right=0, bottom=0)
                )
            ],
            spacing=5,
            padding=ft.Padding(left=25, right=25, top=0, bottom=0),
            auto_scroll=False,
            expand=True
        )
    else:
        scrollable_container = ft.ListView(
            controls=input_rows,
            spacing=5,
            padding=ft.Padding(left=25, right=25, top=0, bottom=0),
            auto_scroll=False,
            expand=True
        )

    # Добавляем колонку на страницу
    page.add(scrollable_container, bottom_app_bar)