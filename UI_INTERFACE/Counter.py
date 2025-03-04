import flet as ft

# Глобальный словарь для хранения текущих значений счетчиков
counter_values = {}


def get_counter_value(counter_id: str):
    """Возвращает текущее значение счетчика по его ID."""
    return counter_values.get(counter_id, None)
def create_counter(
    counter_id: str,
    initial_count: int,
    label: str,
    bgcolor: str = "#222222",
    text_color: str = "white",
    button_color: str = "blue",
    label_font: str = "TikTok Medium",
    count_font: str = "TikTok Bold",
    visible: bool = True  # Добавляем параметр для видимости
) -> ft.Container:
    """Создает контейнер-счетчик с кнопками и текстом."""
    # Инициализируем начальное значение в словаре
    counter_values[counter_id] = initial_count

    # Функция для обновления текста с числом
    def update_count():
        return ft.Text(
            str(counter_values[counter_id]),
            size=40,
            color=text_color,
            font_family=count_font,
            left=10,
            top=40,
        )

    # Общая функция для изменения значения
    def update_value(increment):
        counter_values[counter_id] = max(1, min(99, counter_values[counter_id] + increment))
        square.content.controls[1] = update_count()  # Обновляем текст с числом
        square.update()  # Обновляем контейнер

    # Функция для создания кнопок
    def create_button(icon, top, on_click, splash_radius=1):
        return ft.IconButton(
            icon=icon,
            icon_size=35,
            icon_color=button_color,  # Устанавливаем цвет кнопки
            left=53,
            top=top,
            on_click=on_click,
            splash_radius=splash_radius,
        )

    # Функция для изменения видимости
    def set_visibility(is_visible: bool):
        square.visible = is_visible
        square.update()  # Обновляем контейнер, чтобы изменения применились

    # Создаем контейнер с заданными размерами и цветом фона
    square = ft.Container(
        width=105,
        height=100,
        bgcolor=bgcolor,  # Устанавливаем цвет фона
        border_radius=10,
        visible=visible,  # Устанавливаем начальную видимость
        content=ft.Stack(
            controls=[
                # Текст с описанием
                ft.Text(
                    label,
                    size=12,
                    color=text_color,  # Устанавливаем цвет текста
                    font_family=label_font,
                    width=80,
                    left=10,
                    top=15,
                ),
                # Текст с текущим значением
                update_count(),
                # Кнопки
                create_button(ft.Icons.ADD_CIRCLE, 5, lambda e: update_value(1)),
                create_button(ft.Icons.REMOVE_CIRCLE_OUTLINE, 45, lambda e: update_value(-1)),
            ]
        )
    )

    # Возвращаем контейнер и функцию для изменения видимости
    return square, set_visibility
