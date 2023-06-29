from pandas import read_excel


class RawDataFirstColumnIsIndex:
    """
    Класс для считывания исходных данных без обработки.
    Единственная обработка это использование первого столбца для
    индексации строк.
    """

    def __init__(self, path_to_file, sheet_name):
        try:
            self.data = read_excel(path_to_file, sheet_name=sheet_name)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Не найден файл {path_to_file}"
            )
        except BaseException:
            raise FileNotFoundError(
                f"Файл {path_to_file}или не является таблицей xls, или не"
                f" имеет листа {sheet_name}"
            )
        # Используем первый столбец в качестве индексов строк
        self.data.index = self.data.iloc[:, 0]
        self.data.pop(self.data.columns[0])
