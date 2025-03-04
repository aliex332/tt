import os
import sys
import flet as ft
import webbrowser

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def MainMenuPage(udid, page: ft.Page):
    page.window.width = 1024
    page.window.height = 650
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = True
    page.window.full_screen = False
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#191919"

    try:
        with open(f'{local_path}/resource/Language.txt', 'r') as f: language = f.read().strip()  # Считываем содержимое файла
    except FileNotFoundError: language = ''

    value = language if language else 'EN'

    page.client_storage.set("Localisation", value)
    # page.window.icon = 'E:\Python\PycharmProjects\pythonProject3\\UI_INTERFACE\\assets\photo\\1234566.ico'

    if page.client_storage.get("Localisation") == 'EN':
        text1 = 'Use this action to get new accounts and then interact with them.'
        text2 = 'If you already have registered accounts, use this feature to interact with them.'
        text3 = 'Upload your videos, photos or create camera footage to your account.'
        text4 = 'Use it for mentions, changing your bio, nickname and other on your account.'

    if page.client_storage.get("Localisation") == 'RU':
        text1 = 'Регистрируйте новые аккаунты и затем взаимодействовуйте с ними.'
        text2 = 'Входите в свои аккаунты и затем взаимодействуйте с ними.'
        text3 = 'Загружайте свои видео, фотографии или создавайте записи с камеры.'
        text4 = 'Изменяйте биографиию, никнейм и другие настройки в вашем аккаунте.'

    page.fonts = {
        "TikTok Bold": "fonts/TikTokText-Bold.ttf",
        "TikTok Medium": "fonts/TikTokText-Medium.ttf",
        "TikTok Regular": "fonts/TikTokText-Regular.ttf",
    }

    # Центрирование содержимого
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    setup_button = ft.ElevatedButton(
        text="SETUP DEVICE",  # Текст кнопки
        on_click=lambda e: page.go("/SetupDevice"),  # Обработчик нажатия
        color="white",  # Цвет текста
        bgcolor="blue",  # Изначально серый фон
        disabled=False,  # Кнопка неактивна
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), text_style=ft.TextStyle(font_family='TikTok Medium')),
    )

    def open_url_info(e):
        if page.client_storage.get("Localisation") == 'EN': webbrowser.open('https://google.com', new=2)  # new=2 откроет в новом окне/вкладке
        if page.client_storage.get("Localisation") == 'RU': webbrowser.open('https://google.com', new=2)  # new=2 откроет в новом окне/вкладке


    page.appbar = ft.AppBar(
        title=ft.Text("FIRST CHOOSE TIKTOK MODE", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,  # Отключаем эффект повышения при скролле
        leading=ft.IconButton(
                    ft.Icons.TIPS_AND_UPDATES_OUTLINED,
                    icon_color="green",
                    icon_size=23,
                    tooltip="More information",
                    on_click=lambda e: open_url_info(e)
                ),
        actions=[  # Добавляем контейнер с кнопками в правую часть AppBar
            ft.Container(
                content=setup_button,
                alignment=ft.alignment.center,
                padding=ft.padding.only(right=10),
            ),
        ]
    )

    def change_language():
        if page.client_storage.get("Localisation") == 'EN':
            page.client_storage.set("Localisation", 'RU')
            with open(f'{local_path}/resource/Language.txt', 'w') as f: f.write('RU')
        elif page.client_storage.get("Localisation") == 'RU':
            page.client_storage.set("Localisation", 'EN')
            with open(f'{local_path}/resource/Language.txt', 'w') as f: f.write('EN')
        page.controls.clear()

        # Заново вызываем функцию для построения страницы
        MainMenuPage(udid, page)
        page.update()

    # Функция для создания контейнера с индивидуальным цветом текста и иконки
    def create_container(title, bg_color, icon_name, icon_color, text_color, route, extra_text=""):
        icon = ft.Icon(name=icon_name, size=100, color=icon_color)
        text = ft.Text(title, size=21, color=text_color, font_family="TikTok Bold")
        extra = ft.Text(extra_text, size=14, color=text_color, font_family="TikTok Regular")

        # Контейнер
        container = ft.Container(
            content=ft.Column(
                controls=[
                    text,
                    icon,
                    extra
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=223,
            height=400,
            bgcolor=bg_color,
            border_radius=10,
            ink=True,
            padding=10,
            on_click=lambda e: page.go(route),  # Переход по маршруту
        )

        # Функция для изменения фона, текста и иконки при наведении
        def on_hover(e):
            if e.data == "true":
                e.control.bgcolor = "red"
                e.control.content.controls[0].color = "white"  # Иконка
                e.control.content.controls[1].color = "white"  # Основной текст
                e.control.content.controls[2].color = "white"  # extra_text
            else:
                e.control.bgcolor = bg_color
                e.control.content.controls[0].color = icon_color  # Восстановление иконки
                e.control.content.controls[1].color = text_color  # Восстановление основного текста
                e.control.content.controls[2].color = text_color  # Восстановление extra_text
            e.control.update()

        # Применяем обработчик для каждого контейнера
        container.on_hover = on_hover

        return container

    # Контейнеры с индивидуальными цветами
    containers = [
        create_container("REGISTER", "#f8f8f8", ft.Icons.SUPERVISOR_ACCOUNT_ROUNDED, "black", "black", "/RegisterModePage", text1),
        create_container("LOGIN", "#f8f8f8", ft.Icons.ACCOUNT_CIRCLE_OUTLINED, "black", "black", "/LoginModePage", text2),
        create_container("POST", "#f8f8f8", ft.Icons.TIKTOK, "black", "black", "/UploadModePage", text3),
        create_container("ACTIONS", "#f8f8f8", ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED, "black", "black", "/ActionModePage", text4)
    ]

    # Размещение контейнеров в строке
    containers_row = ft.Row(controls=containers, alignment=ft.MainAxisAlignment.CENTER, spacing=22)
    # Основной макет
    main_layout = ft.Column(
        controls=[
            ft.Container(
                content=containers_row,  # Ваши контейнеры
                padding=ft.Padding(top=50, bottom=0, left=0, right=0)  # Отступ только сверху
            ),
        ],
        expand=True
    )

    lang_button = ft.Row(
            [
                ft.IconButton(
                    ft.Icons.LANGUAGE,
                    icon_color="white",
                    icon_size=26,
                    tooltip="Language",
                    on_click=lambda e: change_language()
                )
            ],
            alignment=ft.MainAxisAlignment.END)

    page.add(main_layout, lang_button)
