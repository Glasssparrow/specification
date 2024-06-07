from pandas import read_excel


def get_data_with_first_column_as_index(path_to_file, sheet_name):
    """
        Класс для считывания исходных данных без обработки.
        Единственная обработка это использование первого столбца для
        индексации строк.
        """
    try:
        data = read_excel(path_to_file, sheet_name=sheet_name)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Не найден файл {path_to_file}"
        )
    except BaseException:
        raise FileNotFoundError(
            f"Файл {path_to_file} или не является таблицей xls, или не"
            f" имеет листа {sheet_name}"
        )
    # Используем первый столбец в качестве индексов строк
    try:
        data.index = data.iloc[:, 0]
    except IndexError:
        raise Exception(f"Вероятно лист {sheet_name} "
                        f"в файле {path_to_file} пуст.")
    data.pop(data.columns[0])
    return data
