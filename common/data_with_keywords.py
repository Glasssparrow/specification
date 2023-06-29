from pandas import read_excel


class DataWithKeywords:
    """Класс для считывания исходных данных с минимальной их обработкой.
    Находит ключевые слова из полученного листа (формируя словарь),
    а также выносит высоту и ширину таблицы в атрибуты"""

    def __init__(self, path_to_file, sheet_name, keys_list,
                 tolerate_key_not_found=False,
                 tolerate_key_in_column_name=False):
        """Конструктор объекта"""
        try:
            self.data = read_excel(path_to_file, sheet_name=sheet_name)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Не найден файл " + path_to_file
            )
        except BaseException:
            raise FileNotFoundError(
                "Файл " + path_to_file +
                "или не является таблицей xls, или не "
                "имеет листа " + sheet_name
            )

        height = len(self.data)
        breadth = len(self.data.columns)
        self.keys = {}
        for word in keys_list:
            self.keys[word] = []
        for x in range(height):
            for y in range(breadth):
                for word in keys_list:
                    if self.data.iloc[x, y] == word:
                        self.keys[word].append((x, y))
                        break
        if not tolerate_key_not_found:
            for word in self.keys.keys():
                if not self.keys[word]:
                    raise ValueError("В файле - " + path_to_file +
                                     "на листе - " + sheet_name +
                                     "не найдено ключевое слово - " + word)
        if not tolerate_key_in_column_name:
            for word in self.keys.keys():
                if word in self.data.columns:
                    raise ValueError(
                        "На листе " + sheet_name +
                        " ключевое слово " + word +
                        " в названии столбца"
                    )
