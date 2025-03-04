import os
import sys
import platform
import flet as ft
from UI_INTERFACE.ResetFiles import ResetFiles
from UI_INTERFACE.Counter import create_counter, counter_values

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def UploadModePage(page: ft.Page):
    if page.client_storage.get("Localisation") == 'EN':
        text1 = "Gallery is used to upload your videos in Video mode. Choose how many videos you need to upload for one account. Before start, check your video folder."
        text2 = "Gallery is used to upload your photos in Photo mode. Choose how many videos you need to upload and how many photos use in one video. Before start, check your photo folder."
        text3 = "Gallery is used to upload your photos in Autocut mode. Choose how many videos you need to upload and how many photos use in one video. Before start, check your photo folder."
        text4 = "Camera and Gallery is used to upload your videos in Overlay mode. Choose how many videos you need to upload. Before start, check your overlay folder and setup your iPhone on shot position."
        text5 = "Camera is used to upload your videos in Record mode. Choose how many videos you need to upload and how much time use in one video. Before start, setup your iPhone on shot position."
        text6 = "Music will be selected randomly from the file for the chosen country. Banned tracks will be removed. Before start, ensure the file exists  for the chosen country and contains links."
        text7 = "Choose how many times to upload videos to one account. After each lap, your iPhone will go to sleep and upload the videos to the same account again for the specified number of laps."

    if page.client_storage.get("Localisation") == 'RU':
        text1 = "Используется для загрузки ваших видео в режиме Video. Выберите, сколько видео вы хотите загрузить на один аккаунт. Перед \nначалом проверьте папку с видео."
        text2 = "Используется для загрузки фото в режиме Photo. Выберите, сколько видео вы хотите загрузить, и сколько фото использовать в одном видео. Перед началом проверьте папку с фото."
        text3 = "Используется для загрузки фото в режиме Autocut. Выберите, сколько видео вы хотите загрузить, и сколько фото использовать в одном видео. Перед началом проверьте папку с фото."
        text4 = "Камера и Галерея используются для записи ваших видео в режиме Overlay. Выберите, сколько видео вы хотите записать и время для одной записи. Перед началом проверьте папку с Overlay."
        text5 = "Камера используется для загрузки ваших видео в режиме записи. Выберите, сколько видео вы хотите записать, и время для одной записи. Перед началом установите iPhone в положение для съемки."
        text6 = "Музыка будет выбрана случайным образом из файла для выбранной страны. Забаненные треки будут удалены. Перед началом убедитесь, что файл для выбранной страны существует и содержит ссылки."
        text7 = "Выберите, сколько раз загружать видео на один аккаунт. После каждого круга ваш iPhone перейдет в спящий режим и снова загрузит видео на тот же аккаунт для указанного количества кругов."

    def UpdateStorage(use_music_switch=None, use_again_switch=None):
        page.client_storage.set("use_again_switch", {"enabled": use_again_switch.value, "sleep_count": counter_values['counter_sleep_count'], "lap_count": counter_values['counter_lap_count']})
        page.client_storage.set("use_music_switch", use_music_switch.value)
        page.client_storage.set("videos_count", counter_values['counter_videos_count'])
        page.client_storage.set("photo_count", counter_values['counter_photo_count'])
        page.client_storage.set("record_time", counter_values['counter_record_time'])

    def SkipUpload():
        page.client_storage.set("UploadSkip", True)
        page.client_storage.set("Upload", False)
        page.client_storage.set("Video", False)
        page.client_storage.set("Photo", False)
        page.client_storage.set("Autocut", False)
        page.client_storage.set("Overlay", False)
        page.client_storage.set("Record", False)
        page.client_storage.set("use_music_switch", False)
        page.client_storage.set("use_again_switch", {"enabled": use_again_switch.value, "sleep_count": counter_values['counter_sleep_count'], "lap_count": counter_values['counter_lap_count']})
        page.client_storage.set("videos_count", False)
        page.client_storage.set("photo_count", False)
        page.client_storage.set("record_time", False)

    def BackButton():
        if page.client_storage.get("Register") is True: page.go('/RegisterModePage')
        elif page.client_storage.get("Login") is True: page.go('/LoginModePage')
        else: page.go('/MainMenuPage')

    def OpenFolder():
        if platform.system() == "Windows": os.startfile(f'{local_path}/iPhoneTikTokFiles/{last_active_switch["folder_path"]}/')
        if platform.system() == "Darwin": os.system(f'open {local_path}/iPhoneTikTokFiles/{last_active_switch["folder_path"]}/')

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

    # Создаем кнопку NEXT
    next_button = ft.ElevatedButton(
        text="NEXT",  # Текст кнопки
        on_click=lambda e: (UpdateStorage(use_music_switch, use_again_switch), page.go("/ActionModePage")),
        color="white",  # Цвет текста
        bgcolor="red",  # Изначально серый фон
        disabled=False,  # Кнопка неактивна
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            text_style=ft.TextStyle(font_family='TikTok Medium'),
        ),
    )

    # Создаем кнопку SKIP
    skip_button = ft.TextButton(
        text="SKIP",  # Текст кнопки
        on_click=lambda e: (SkipUpload(), page.go("/ActionModePage")),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            text_style=ft.TextStyle(font_family='TikTok Bold'),
            color='#d6d6d6'
        ),
    )

    # Создаем контейнер для кнопок
    buttons_container = ft.Row(
        controls=[
            skip_button,
            next_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Выравнивание по центру
        spacing=10,  # Отступ между кнопками
    )

    # Создаем AppBar с добавлением контейнера для кнопок
    page.appbar = ft.AppBar(
        title=ft.Text("SETUP UPLOAD MODE", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,  # Отключаем эффект повышения при скролле
        leading=ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=lambda e: BackButton()),
        actions=[  # Добавляем контейнер с кнопками в правую часть AppBar
            ft.Container(
                content=buttons_container,
                alignment=ft.alignment.center,
                padding=ft.padding.only(right=10),
            )
        ]
    )

    last_active_switch = {"name": 'Video', "folder_path": 'Videos'}

    def handle_segment_change(event, source=None):
        # Словари с текстами и изображениями
        if source == 'buttons':
            texts = {
                "0": text1,
                "1": text2,
                "2": text3,
                "3": text4,
                "4": text5,
            }

            images = {
                "0": f"{local_path}/resource/assets/photo/Video.png",
                "1": f"{local_path}/resource/assets/photo/Photo.png",
                "2": f"{local_path}/resource/assets/photo/Autocut.png",
                "3": f"{local_path}/resource/assets/photo/Overlay.png",
                "4": f"{local_path}/resource/assets/photo/Record.png",
            }

            base_text = texts.get(event.data)
            base_image = images.get(event.data)
            if event.data == "0":
                last_active_switch["name"] = "Video"
                last_active_switch["folder_path"] = "Videos"
                folder_button.visible = True
                recover_button.visible = False

                page.client_storage.set("Video", True)
                page.client_storage.set("Photo", False)
                page.client_storage.set("Autocut", False)
                page.client_storage.set("Overlay", False)
                page.client_storage.set("Record", False)

                set_videos_visibility(True)
                set_photo_visibility(False)
                set_record_visibility(False)
            elif event.data == "1":
                last_active_switch["name"] = "Photo"
                last_active_switch["folder_path"] = "Photos"
                folder_button.visible = True
                recover_button.visible = False

                page.client_storage.set("Video", False)
                page.client_storage.set("Photo", True)
                page.client_storage.set("Autocut", False)
                page.client_storage.set("Overlay", False)
                page.client_storage.set("Record", False)

                set_videos_visibility(True)
                set_photo_visibility(True)
                set_record_visibility(False)
            elif event.data == "2":
                last_active_switch["name"] = "Autocut"
                last_active_switch["folder_path"] = "Autocut"
                folder_button.visible = True
                recover_button.visible = False

                page.client_storage.set("Video", False)
                page.client_storage.set("Photo", False)
                page.client_storage.set("Autocut", True)
                page.client_storage.set("Overlay", False)
                page.client_storage.set("Record", False)

                set_videos_visibility(True)
                set_photo_visibility(True)
                set_record_visibility(False)
            elif event.data == "3":
                last_active_switch["name"] = "Overlay"
                last_active_switch["folder_path"] = "Overlay"
                folder_button.visible = True

                page.client_storage.set("Video", False)
                page.client_storage.set("Photo", False)
                page.client_storage.set("Autocut", False)
                page.client_storage.set("Overlay", True)
                page.client_storage.set("Record", False)

                set_videos_visibility(True)
                set_photo_visibility(False)
                set_record_visibility(True)
            elif event.data == "4":
                last_active_switch["name"] = "Record"
                last_active_switch["folder_path"] = "Record"
                folder_button.visible = False
                recover_button.visible = False

                page.client_storage.set("Video", False)
                page.client_storage.set("Photo", False)
                page.client_storage.set("Autocut", False)
                page.client_storage.set("Overlay", False)
                page.client_storage.set("Record", True)

                set_videos_visibility(True)
                set_photo_visibility(False)
                set_record_visibility(True)


        if source == 'use_music_switch':
            base_text = text6
            base_image = f"{local_path}/resource/assets/photo/Music.png"
            last_active_switch["name"] = "use_music_switch"
            last_active_switch["folder_path"] = "/AccountsSettings/Music"
            folder_button.visible = True
            recover_button.visible = True

        if source == 'use_again_switch':
            base_text = text7
            base_image = f"{local_path}/resource/assets/photo/UseAgain.png"
            if event.data == 'true': set_sleep_visibility(True); set_lap_visibility(True)
            if event.data == 'false': set_sleep_visibility(False); set_lap_visibility(False)
            folder_button.visible = False
            recover_button.visible = False


        text_content.value = base_text
        image_container.content = ft.Image(src=base_image)
        page.update()

    # Элементы для сегментированной кнопки
    segmented_button = ft.CupertinoSegmentedButton(
        selected_index=0,
        border_color='black',
        click_color='white',
        unselected_color='#ecf0f1',
        selected_color='black',
        on_change=lambda e: handle_segment_change(e, source='buttons'),  # Подключаем функцию
        controls=[
            ft.Container(
                padding=ft.padding.symmetric(0, 30),
                content=ft.Text("Video"),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 30),
                content=ft.Text("Photo"),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 30),
                content=ft.Text("Autocut"),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 30),
                content=ft.Text("Overlay"),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 30),
                content=ft.Text("Record"),
            ),
        ],
        top=50,
        left=371
    )

    # Контейнер с изображением (он будет виден поверх других элементов)
    image_container = ft.Container(
        content=ft.Image(src=f"{local_path}/resource/assets/photo/Video.png",),
        left=-120,  # Горизонтальное смещение
        top=-120,   # Верхнее смещение
    )

    text_content = ft.Text(text1, size=16, font_family="TikTok Regular")

    folder_button = ft.IconButton(
        icon=ft.Icons.FOLDER_COPY_OUTLINED,  # Иконка
        icon_size=30,
        tooltip="Open folder",
        on_click=lambda e: OpenFolder(),  # Обработчик клика
        icon_color="white",  # Цвет иконки
        visible=True
    )

    recover_button = ft.IconButton(
        icon=ft.Icons.AUTO_DELETE_OUTLINED,  # Иконка
        icon_size=30,
        tooltip="Reset settings",
        on_click=lambda e: RecoverFolder(),  # Обработчик клика
        icon_color="white",  # Цвет иконки
        visible=False
    )

    text_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=text_content,
                    padding=ft.padding.only(bottom=0),
                ),
                ft.Row(  # Добавил row для folder_button
                    controls=[
                        folder_button,
                        recover_button
                    ],
                ),
            ],
            spacing=10,  # Расстояние между текстом и иконкой
        ),
        width=400,  # Ширина контейнера
        alignment=ft.alignment.center,  # Выравнивание текста и иконки
        padding=ft.padding.all(10),  # Отступы внутри контейнера
        left=380,  # Горизонтальное смещение контейнера
        top=120,  # Вертикальное смещение контейнера
    )

    videos_count, set_videos_visibility = create_counter("counter_videos_count", 6, "Videos count:", "white", "black", "black", visible=True)
    photo_count, set_photo_visibility = create_counter("counter_photo_count", 3, "Photo in video:", "white", "black", "black", visible=False)
    record_time, set_record_visibility = create_counter("counter_record_time", 7, "Record seconds:", "white", "black", "black", visible=False)
    sleep_count, set_sleep_visibility = create_counter("counter_sleep_count", 25, "Sleep minutes:", "blue", "white", "white", visible=False)
    lap_count, set_lap_visibility = create_counter("counter_lap_count", 2, "Laps counter:", "blue", "white", "white", visible=False)

    buttons_container = ft.Container(
        content=ft.Column(
            controls=[
                videos_count,
                photo_count,
                record_time,
                sleep_count
            ],
            spacing=10,  # Отступ между `Row` в `Column`
            alignment=ft.MainAxisAlignment.START,  # Выравнивание по началу
        ),
        alignment=ft.alignment.center,  # Выравнивание контейнера по центру
        top=133,  # Смещение вниз
        left=835,  # Смещение вправо
    )

    second_buttons_container = ft.Container(
        content=ft.Column(
            controls=[
                lap_count
            ],
            spacing=10,  # Отступ между `Row` в `Column`
            alignment=ft.MainAxisAlignment.START,  # Выравнивание по началу
        ),
        alignment=ft.alignment.center,  # Выравнивание контейнера по центру
        top=244,  # Смещение вниз
        left=719,  # Смещение вправо
    )

    # Контейнер с двумя свитчами
    use_music_switch = ft.Switch(
        value=False,
        label="Use music ",
        label_position=ft.LabelPosition.LEFT,
        thumb_color=ft.Colors.WHITE,
        track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY},
        focus_color=ft.Colors.PURPLE,
        label_style=ft.TextStyle(size=18, font_family="TikTok Bold"),
        on_change=lambda e: handle_segment_change(e, 'use_music_switch'),  # Обработчик для свитча
    )

    use_again_switch = ft.Switch(
        value=False,
        label="Use again ",
        label_position=ft.LabelPosition.LEFT,
        thumb_color=ft.Colors.WHITE,
        track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY},
        focus_color=ft.Colors.PURPLE,
        label_style=ft.TextStyle(size=18, font_family="TikTok Bold"),
        on_change=lambda e: handle_segment_change(e, 'use_again_switch'),  # Обработчик для свитча
    )

    # Контейнер для размещения свитчей
    switches_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LIBRARY_MUSIC, size=22, color=ft.Colors.GREEN),  # Иконка музыки
                        use_music_switch,
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.TIMER, size=22, color=ft.Colors.BLUE),  # Иконка таймлапса
                        use_again_switch,
                    ]
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
        ),
        left=383,  # Горизонтальное смещение
        top=350,  # Вертикальное смещение
    )

    # Основной Stack
    stack = ft.Stack(
        controls=[
            image_container,  # Изображение будет первым в списке (оно будет на фоне)
            segmented_button,
            text_container,
            switches_container,
            buttons_container,
            second_buttons_container# Добавляем контейнер с свитчами
        ],
    )

    page.add(stack)
