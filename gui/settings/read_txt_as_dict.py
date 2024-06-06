

def is_string_a_number(string):
    """
    Возвращает True если строка состоит только из цифр и имеет не более одной точки.
    В противном случае возвращает False.
    Поднимает ошибку если передана не строка.
    """
    if not isinstance(string, str):
        raise ValueError("is_string_a_number принимает только строки.")
    dots = 0
    have_only_numbers = True
    for x in string:
        if x == ".":
            dots += 1
        elif x not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            have_only_numbers = False
    if dots < 2 and have_only_numbers:
        return True
    else:
        return False


def read_as_dict(path: str, splitter=": ", list_splitter=",",
                 open_brackets="[", close_bracket="]",
                 allow_broken_strings=False):
    """
    Функция читающая файл и возвращающая словарь.
    Всё что до разделителя - ключ.
    Всё что после разделителя - значение.
    Всё что после второго разделителя - комментарии,
    которые функция не будет читать.
    Пробелы в начале и конце ключа и значения удаляются.
    """
    dictionary = {}
    # Читаем файл
    file = open(path, "r", encoding="utf-8")
    try:
        text = file.read()
    finally:
        file.close()
    # Делим текст на строки
    text_list = text.split("\n")
    # Проходимся по каждой строке.
    # Берем первые два элемента листа. 0 - ключ, 1 - значение
    # Проверяем есть ли открывающая скобка в начале значения.
    # Обрезаем скобки и нарезаем значение на элементы листа.
    for x in text_list:
        # Пропускаем строку если она пуста
        if not x.strip():
            continue
        key_and_value = x.split(splitter)[0:2]
        # Должен получиться лист минимум из 2 элементов.
        # Если это не так, то это ошибка заполнение, пропускаем строку.
        if len(key_and_value) < 2:
            # Поднимаем ошибку если неверно заполненные строки не разрешены.
            if not allow_broken_strings:
                raise ValueError("Не найден разделитель строки")
            continue
        # Удаляем пустоты между элементами т.к.
        # с пустотами заполнять файл удобнее, а вот
        # при выполнении программы они мешают.
        key = key_and_value[0].strip()
        value = key_and_value[1].strip()
        if is_string_a_number(value):
            value = float(value)
        elif value[0] == open_brackets:
            if value[len(value)-1] == close_bracket:
                value = value[1:-1]
            else:
                value = value[1:]
            value = value.split(list_splitter)
            # Снова избавляемся от пустот.
            for y in range(len(value)):
                value[y] = value[y].strip()
            list_of_digits = True
            for y in range(len(value)):
                if is_string_a_number(value[y]):
                    pass
                else:
                    list_of_digits = False
            if list_of_digits:
                new_value = []
                for list_element in range(len(value)):
                    new_value.append(float(value[list_element]))
                value = new_value
        # К этому моменту value должно либо остаться строкой,
        # либо стать листом.
        dictionary[key] = value
    return dictionary
