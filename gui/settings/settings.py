from .write_dict_as_txt import write_to_txt_from_dict


def return_settings_to_default():

    settings = {
        "Путь по умолчанию": "C:/",

        "Приоритет сортировки по умолчанию": 3,
        "Название итогового файла": "Посчитанная спецификация",
        "Название листа спецификации в итоговом файле": "Спецификация",
        "Метка обычного узла": "node",
        "Метка подузла": "subnode",
        "Метка особого узла с нумерацией материалов": "ol",
        "Метка особого узла без нумерации материалов": "ul",
        "Метка особого узла с дополнительным уровнем нумерации": "num",
        "Метка количества узлов": "key",
    }

    settings_specification = {
        "Лист метаданных": "Метаданные",
        "Столбец с типами листов": "Тип",
        "Ключевое слово для листов с количеством узлов": "спецификация",
        "Ключевое слово для листов с узлами": "узлы",
        "Ключевое слово для листов с локальной библиотекой": "библиотека",
    }

    settings_library = {

        "Путь к основной библиотеке": "Library.xlsx",

        # Данные для чтения метаданных
        "Лист метаданных основной библиотеки": "Категории",
        "Столбец названий листов": "Sheet name",
        "Столбец приоритета сортировки подкатегории": "Sort priority",
        "Столбец метки подкатегории по умолчанию": "Is default subcategory",
        "Столбец категории": "Category",
        "Столбец названия категории": "Category name",
        "Столбец приоритета сортировки категории": "Category priority",
        "Столбец метки категории по умолчанию": "Is default category",

        # Данные для чтения библиотеки
        "Столбец приоритета сортировки": "Приоритет",
        "Столбец с меткой для материалов с множителем": "Есть множитель",
        "Столбец наименования": "Наименование",
        "Столбец обозначения": "Обозначение",
        "Столбец кода оборудования": "Код",
        "Столбец производителя": "Производитель",
        "Столбец единицы измерения": "Единица измерения",
        "Столбец массы": "Масса",
        "Столбец примечания": "Примечание",

        # Колонка уникальная для локальной библиотеки
        "Столбец подкатегории материала": "Категория"
    }

    write_to_txt_from_dict("settings/Основные настройки.txt",
                           settings, ": ",
                           list_splitter=", ")
    write_to_txt_from_dict("settings/Настройки спецификации.txt",
                           settings_specification, ": ",
                           list_splitter=", ")
    write_to_txt_from_dict("settings/Настройки библиотеки.txt",
                           settings_library, ": ",
                           list_splitter=", ")
