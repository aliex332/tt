import os
import sys
import platform
import flet as ft

def VpnManager(page: ft.Page):
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
        title=ft.Text("VPN MANAGER", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,
        leading=ft.IconButton(ft.Icons.CLOSE, on_click=lambda e: CloseButton()),
        actions=[
            ft.Container(
                content=ft.IconButton(ft.Icons.NETWORK_CHECK_SHARP, on_click=lambda e: page.go('/ProxyManager'), tooltip='PROXY Manager'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(ft.Icons.MARK_EMAIL_UNREAD_OUTLINED, on_click=lambda e: page.go('/ImapManager'), tooltip='IMAP Manager'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(ft.Icons.SWITCH_ACCOUNT_OUTLINED, on_click=lambda e: page.go('/AccountManager'), tooltip='Account Manager'),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
            ft.Container(
                content=ft.IconButton(icon=ft.Icons.FOLDER_COPY_OUTLINED, icon_size=24, tooltip="VPN Folder", on_click=lambda e: OpenFolder('iPhoneNetSettings/VPN'), icon_color="blue"),
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            ),
        ]
    )


    vpn_number = ft.IconButton(
        icon=ft.Icons.FILTER_LIST_OUTLINED,
        icon_color="white",
        disabled=True
    )

    def update_save_button_state():
        if name_field.value: save_button.disabled = False; save_button.icon_color = '#1dd1a1'  # Активируем кнопку
        else: save_button.disabled = True; save_button.icon_color = 'white'
        page.update()  # Обновляем интерфейс

    def save_button_clicked(e):
        vpn_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.INFO_OUTLINED, size=30, color='orange'),
                    ft.Text(f"Please follow these steps:", size=20, font_family="TikTok Bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            content=ft.Column(
                [
                    ft.Text(
                        f"1. Download your .ovpn configs from your VPN Provider.\n"
                        f"2. Rename these config files as follows: 'YourName_{name_field.value}'.\n"
                        "3. Organize these configs by country code in the 'COUNTRY' folder.\n\n"
                        "After this, check visibility for your VPN configs in 'Account Manager'.",
                        size=16,
                        font_family="TikTok Regular"
                    ),
                ],
                spacing=10,
                tight=True,
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: (setattr(vpn_dialog, "open", False), page.update())),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(vpn_dialog)
        vpn_dialog.open = True
        page.update()

        if login_field.value.strip() == '': login_field.value = 'NONE'
        if password_field.value.strip() == '': password_field.value = 'NONE'
        vpn_data = f'{name_field.value}:{login_field.value}:{password_field.value}'.rstrip(':')
        with open(f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/VPNServices.txt", "r+") as file:
            existing_data = [line.strip() for line in file if line.strip()]  # Чистим пробелы и пустые строки
            file.seek(0)  # Возвращаемся в начало файла
            file.write(f"{vpn_data}\n")  # Добавляем новую строку
            file.writelines(f"{line}\n" for line in existing_data)  # Перезаписываем остальные строки
            file.truncate()  # Удаляем лишние данные, если файл стал короче
        update_ui(scrollable_container)
        name_field.value = ''
        login_field.value = ''
        password_field.value = ''
        save_button.icon_color = 'white'
        save_button.disabled = True
        page.update()

    name_field = ft.TextField(
        label=ft.Text("VPN Name", color='white', font_family="TikTok Regular", size=15),
        width=150,
        border_color='white',
        prefix_icon=ft.Icon(ft.Icons.VPN_LOCK, color="white"),
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
            vpn_number,
            name_field,
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


    def GetVPNBase():
        with open(f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/VPNServices.txt") as f:  ## Открываем файл
            lines = [line.strip() for line in f]
            return lines

    def GetVPNFromBase(vpn_data):
        vpn_data = vpn_data.split(':')
        return vpn_data[0], vpn_data[1], vpn_data[2]

    def delete_account(delete_data, scrollable_container):
        delete_data = delete_data.replace(':None', '').strip()  # Удаляем ':None' и обрезаем пробелы

        # Читаем все аккаунты из файла
        vpn = GetVPNBase()

        # Удаляем строку с нужным аккаунтом (сравнение по обрезанным строкам)
        updated_accounts = [account.strip() for account in vpn if account.strip() != delete_data]

        # Перезаписываем файл без удаленной строки
        with open(f"{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/VPNServices.txt", 'w') as f:
            for account in updated_accounts: f.write(f"{account}\n")

        # Обновляем UI с уже обновленными данными
        update_ui(scrollable_container)

    def create_empty_message():
        """Создаёт контейнер с сообщением о пустом списке."""
        return ft.Container(
            content=ft.Text(
                "Your VPN list is empty!\nAdd your VPN providers here before using...",
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
        updated_vpn = GetVPNBase()

        # Создаем строки ввода для каждого аккаунта
        input_rows = [create_input_row(i, account) for i, account in enumerate(updated_vpn)]

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


    def create_input_row(index, vpn_data):
        vpn_name, vpn_login, vpn_pass = GetVPNFromBase(vpn_data)
        delete_data = f'{vpn_name}:{vpn_login}:{vpn_pass}'

        vpn_number = ft.Text(
            f"{index + 1}",
            color="#dfe6e9",
            size=16,
            weight=ft.FontWeight.BOLD,
            width=30,
            text_align=ft.TextAlign.CENTER,
            font_family="TikTok Bold"
        )

        name_field = ft.TextField(
            label=ft.Text('VPN Name', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            value=vpn_name,
            text_style=ft.TextStyle(color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            read_only=True
        )

        login_field = ft.TextField(
            label=ft.Text('Login', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            prefix_icon=ft.Icon(ft.Icons.PERSON, color="#b2bec3", visible=False),
            value=vpn_login,
            text_style=ft.TextStyle(color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            read_only=True
        )

        password_field = ft.TextField(
            label=ft.Text('Password', text_align=ft.TextAlign.CENTER, color="#b2bec3", weight=ft.FontWeight.NORMAL, font_family="TikTok Regular"),
            width=150,
            border_color="#636e72",
            prefix_icon=ft.Icon(ft.Icons.LOCK, color="#b2bec3", visible=False),
            value=vpn_pass,
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
                vpn_number,
                name_field,
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
    vpn = GetVPNBase()

    # Создаем строки ввода для каждого аккаунта
    input_rows = [create_input_row(i, account) for i, account in enumerate(vpn)]
    if not input_rows:
        scrollable_container = ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Your VPN list is empty!\nAdd your VPN providers here before using...",
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
            padding=ft.Padding(left=160, right=160, top=0, bottom=0),
            auto_scroll=False,
            expand=True
        )
    else:
        scrollable_container = ft.ListView(
            controls=input_rows,
            spacing=5,
            padding=ft.Padding(left=160, right=160, top=0, bottom=0),
            auto_scroll=False,
            expand=True
        )

    # Добавляем колонку на страницу
    page.add(scrollable_container, bottom_app_bar)