import flet as ft
import sys
import os
import platform
from iPhoneTikTokCheckers.AccountsDataBase import GetAccountFromBase

def AccountManager(page: ft.Page):
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

    selected_option = None
    imap_data = None

    page.appbar = ft.AppBar(
        title=ft.Text("ACCOUNT MANAGER", size=24, color='white', font_family="TikTok Bold"),
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
                content=ft.IconButton(ft.Icons.NETWORK_CHECK_SHARP, on_click=lambda e: page.go('/ProxyManager'), tooltip='PROXY Manager'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(ft.Icons.MARK_EMAIL_UNREAD_OUTLINED, on_click=lambda e: page.go('/ImapManager'), tooltip='IMAP list'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(icon=ft.Icons.FOLDER_COPY_OUTLINED, icon_size=24, tooltip="Accounts Folder", on_click=lambda e: OpenFolder('AccountsDataBase'), icon_color="blue"),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
        ]
    )

    def configure_imap_dialog(e, page):
        nonlocal imap_data; imap_data = None
        if e.control.value == "No email": imap_data = None; return True

        login_field = ft.TextField(
            label=ft.Text('Login', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=300,
            border_color='#636e72',
            hint_text='Enter login...',
            prefix_icon=ft.Icon(ft.Icons.PERSON_OUTLINE),
            on_change=lambda e: update_ok_button_state()
        )

        password_field = ft.TextField(
            label=ft.Text('Password', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            password=True,
            width=300,
            border_color='#636e72',
            hint_text='Enter password...',
            prefix_icon=ft.Icon(ft.Icons.LOCK_OUTLINE),
            on_change=lambda e: update_ok_button_state()
        )

        domain_field = ft.TextField(
            label=ft.Text('Domain', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=300,
            border_color='#636e72',
            hint_text='Enter domain...',
            prefix_icon=ft.Icon(ft.Icons.LINK_OUTLINED),
            on_change=lambda e: update_ok_button_state()
        )

        port_field = ft.TextField(
            label=ft.Text('Port', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=300,
            border_color='#636e72',
            hint_text='Enter port...',
            prefix_icon=ft.Icon(ft.Icons.WIFI_TETHERING),
            on_change=lambda e: update_ok_button_state()
        )

        # Функция для обновления состояния кнопки OK
        def update_ok_button_state():
            if all([login_field.value, password_field.value, domain_field.value, port_field.value]): imap_dialog.actions[0].disabled = False  # Активируем кнопку OK
            else: imap_dialog.actions[0].disabled = True  # Делаем кнопку OK неактивной
            page.update()

        # Обработка нажатия OK
        def on_ok(e):
            nonlocal imap_data
            imap_data = f"IMAP:{login_field.value}:{password_field.value}:{domain_field.value}:{port_field.value}"
            email_dropdown.value = "IMAP"
            imap_dialog.open = False
            page.update()

        # Обработка нажатия Cancel
        def on_cancel(e):
            nonlocal imap_data
            imap_data = "No email"
            imap_dialog.open = False
            email_dropdown.value = imap_data
            page.update()

        # Создаем AlertDialog
        imap_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.MARK_EMAIL_UNREAD_OUTLINED, size=30, color='orange'),  # Иконка email
                    ft.Text("IMAP Settings:", size=20, font_family="TikTok Bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            content=ft.Column(
                [
                    login_field,
                    password_field,
                    domain_field,
                    port_field,
                ],
                spacing=10,
                tight=True,
            ),
            actions=[
                ft.TextButton("OK", on_click=on_ok, disabled=True),  # Кнопка OK изначально неактивна
                ft.TextButton("Cancel", on_click=on_cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Показываем диалог
        page.overlay.append(imap_dialog)
        imap_dialog.open = True
        page.update()

    # Dropdown с обработкой выбора
    email_dropdown = ft.Dropdown(
        width=120,
        options=[
            ft.dropdown.Option("IMAP"),
            ft.dropdown.Option("No email")
        ],
        hint_content=ft.Row(
            [
                ft.Icon(ft.Icons.EMAIL, color="white"),
                ft.Text("Email", text_align=ft.TextAlign.CENTER, color="white", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        border_color="white",
        text_size=15,
        on_change=lambda e: configure_imap_dialog(e, page)
    )

    account_number = ft.IconButton(
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

    def on_security_select(e, selected_security, selected_country):
        if e.control.value == "No security": nonlocal selected_option; selected_option = None; return True

        def on_cancel(e):
            vpn_dialog.open = False
            security_dropdown.value = "No security"
            page.update()

        def on_ok(e):
            nonlocal selected_option
            selected_option = f"{selected_security}:{selected_option}"
            selected_option = selected_option.replace(f'{country_code}:', '').rstrip()
            vpn_dialog.open = False
            page.update()

        if selected_country is None or selected_country == "":
            vpn_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Row(
                [
                    ft.Icon(ft.Icons.LOCK_OUTLINE_ROUNDED, size=30, color='orange'),  # Иконка email
                    ft.Text(f"{selected_security} Settings:", size=20, font_family="TikTok Bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
                content=ft.Column(
                    [
                        ft.Text(f"Before choosing a {selected_security}, please set up a country.", size=16, font_family="TikTok Regular"),
                    ],
                    spacing=10,
                    tight=True,
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=on_cancel),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        else:
            country_code = country_iso2.get(selected_country)
            folder_path = f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/{selected_security}"
            matching_lines = []

            if selected_security == "VPN":
                folder_path = f"{folder_path}/COUNTRY/{country_code}"
                if os.path.isdir(folder_path):
                    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                    matching_lines = [f"{os.path.splitext(f)[0]}" for f in files]
            elif selected_security == "PROXY":
                file_path = f"{folder_path}/Proxy.txt"
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        for line in file:
                            parts = line.strip().split(":")
                            if parts[0] == country_code:
                                matching_lines.append(line.strip())

            if not matching_lines:
                vpn_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Row(
                        [
                            ft.Icon(ft.Icons.WARNING, size=30, color='red'),  # Иконка email
                            ft.Text(f"Error configurations not found!", size=20, font_family="TikTok Bold"),
                        ]),
                    content=ft.Column(
                        [
                            ft.Text(
                                f"{selected_security} configurations are not available for '{selected_country}'."
                                f"\nPlease add the necessary configuration in {selected_security} manager.",
                                size=16,
                                font_family="TikTok Regular"
                            ),
                        ],
                        spacing=10,
                        tight=True,
                    ),
                    actions=[
                        ft.TextButton("Cancel", on_click=on_cancel),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            else:
                dropdown_options = [ft.dropdown.Option(option) for option in matching_lines]

                def on_dropdown_change(e):
                    nonlocal selected_option
                    selected_option = e.control.value
                    vpn_dialog.actions[0].disabled = not selected_option
                    page.update()

                vpn_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCK_OUTLINE_ROUNDED, size=30, color='orange'),  # Иконка email
                            ft.Text(f"{selected_security} Settings:", size=20, font_family="TikTok Bold"),
                        ]),
                    content=ft.Column(
                        [
                            ft.Text(f"Selected country: {selected_country}", size=16, font_family="TikTok Regular"),
                            ft.Dropdown(
                                options=dropdown_options,
                                hint_content=ft.Text(f"Choose {selected_security}", font_family="TikTok Regular"),
                                border_color="#636e72",
                                text_size=15,
                                on_change=on_dropdown_change,
                            ),
                        ],
                        spacing=10,
                        tight=True,
                        width=350
                    ),
                    actions=[
                        ft.TextButton("OK", on_click=on_ok, disabled=True),
                        ft.TextButton("Cancel", on_click=on_cancel),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

        page.overlay.append(vpn_dialog)
        vpn_dialog.open = True
        page.update()


    # security_dropdown - выпадающий список для выбора типа безопасности
    security_dropdown = ft.Dropdown(
        width=135,
        options=[
            ft.dropdown.Option("VPN"),
            ft.dropdown.Option("PROXY"),
            ft.dropdown.Option("No security")
        ],
        hint_content=ft.Row(
            [
                ft.Icon(ft.Icons.LOCK_ROUNDED, color="white"),
                ft.Text("Security", text_align=ft.TextAlign.CENTER, color="white", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        border_color="white",
        text_size=15,
        on_change=lambda e: on_security_select(e, security_dropdown.value, country_dropdown.value),  # Передаем текущие значения
    )

    def update_save_button_state():
        if login_field.value and password_field.value and country_dropdown.value: save_button.disabled = False; save_button.icon_color = '#1dd1a1'  # Активируем кнопку
        else: save_button.disabled = True; save_button.icon_color = 'white'
        page.update()  # Обновляем интерфейс

    def save_button_clicked(e):
        nonlocal imap_data
        nonlocal selected_option
        country_code = country_iso2.get(country_dropdown.value)
        account_data = f'{country_code}:{login_field.value}:{password_field.value}:{imap_data}:{selected_option}'.replace(':None', '').replace(':No email', '').replace(':No Security', '').rstrip(':')
        with open(f"{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt", "r+") as file:
            existing_data = [line.strip() for line in file if line.strip()]  # Чистим пробелы и пустые строки
            file.seek(0)  # Возвращаемся в начало файла
            file.write(f"{account_data}\n")  # Добавляем новую строку
            file.writelines(f"{line}\n" for line in existing_data)  # Перезаписываем остальные строки
            file.truncate()  # Удаляем лишние данные, если файл стал короче
        update_ui(scrollable_container)
        country_dropdown.value = ''
        login_field.value = ''
        password_field.value = ''
        email_dropdown.value = ''
        security_dropdown.value = ''
        imap_data = None
        selected_option = None
        save_button.icon_color = 'white'
        save_button.disabled = True
        page.update()


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
            account_number,
            country_dropdown,
            login_field,
            password_field,
            email_dropdown,
            security_dropdown,
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


    def GetAccountBase():
        with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt') as f:  ## Открываем файл
            lines = [line.strip() for line in f]
            return lines

    def delete_account(delete_data, scrollable_container):
        delete_data = delete_data.replace(':None', '').strip()  # Удаляем ':None' и обрезаем пробелы

        # Читаем все аккаунты из файла
        accounts = GetAccountBase()

        # Удаляем строку с нужным аккаунтом (сравнение по обрезанным строкам)
        updated_accounts = [account.strip() for account in accounts if account.strip() != delete_data]

        # Перезаписываем файл без удаленной строки
        with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt', 'w') as f:
            for account in updated_accounts:
                f.write(f"{account}\n")

        # Обновляем UI с уже обновленными данными
        update_ui(scrollable_container)

    def create_empty_message():
        """Создаёт контейнер с сообщением о пустом списке."""
        return ft.Container(
            content=ft.Text(
                "Your account list is empty! Add your accounts here\nor register them before starting...",
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
        updated_accounts = GetAccountBase()

        # Создаем строки ввода для каждого аккаунта
        input_rows = [create_input_row(i, account) for i, account in enumerate(updated_accounts)]

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


    def create_input_row(index, account_data):
        country_code, account_data, EMAIL, NETWORK, NETWORK_DATA = GetAccountFromBase(account_data)
        if EMAIL != None: EMAIL = f'IMAP:{EMAIL}'
        delete_data = f'{country_code}:{account_data}:{EMAIL}:{NETWORK}:{NETWORK_DATA}'
        country_name = next((name for name, iso2 in country_iso2.items() if iso2 == country_code), None)

        account_number = ft.Text(
            f"{index + 1}",
            color="#dfe6e9",
            size=16,
            weight=ft.FontWeight.BOLD,
            width=30,
            text_align=ft.TextAlign.CENTER,
            font_family="TikTok Bold"
        )

        country_dropdown_value = country_name
        tiktok_login_value = account_data.split(":")[0]
        tiktok_password_value = account_data.split(":")[1]
        email_dropdown_value = "IMAP" if EMAIL else "No email"
        security_dropdown_value = NETWORK if NETWORK else "No security"

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

        email_dropdown = ft.Dropdown(
            width=120,
            hint_content=ft.Row(
                [
                    ft.Text(email_dropdown_value, text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            border_color="#636e72",
            text_size=15,
            value=email_dropdown_value
        )

        security_dropdown = ft.Dropdown(
            width=135,
            hint_content=ft.Row(
                [
                    ft.Text(security_dropdown_value, text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            border_color="#636e72",
            text_size=15,
            value=security_dropdown_value
        )

        login_field = ft.TextField(
            label=ft.Text('Login', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            prefix_icon=ft.Icon(ft.Icons.PERSON, color="#b2bec3", visible=False),
            value=tiktok_login_value,
            text_style=ft.TextStyle(color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            read_only=True
        )

        password_field = ft.TextField(
            label=ft.Text('Password', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            prefix_icon=ft.Icon(ft.Icons.LOCK, color="#b2bec3", visible=False),
            value=tiktok_password_value,
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
                account_number,
                country_dropdown,
                login_field,
                password_field,
                email_dropdown,
                security_dropdown,
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
    accounts = GetAccountBase()

    # Создаем строки ввода для каждого аккаунта
    input_rows = [create_input_row(i, account) for i, account in enumerate(accounts)]
    if not input_rows:
        scrollable_container = ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Your account list is empty! Add your accounts here\nor register them before starting...",
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
            padding=ft.Padding(left=45, right=45, top=0, bottom=0),
            auto_scroll=False,
            expand=True
        )
    else:
        scrollable_container = ft.ListView(
            controls=input_rows,
            spacing=5,
            padding=ft.Padding(left=45, right=45, top=0, bottom=0),
            auto_scroll=False,
            expand=True
        )

    # Добавляем колонку на страницу
    page.add(scrollable_container, bottom_app_bar)