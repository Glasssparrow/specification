from pandas import isna, DataFrame


class RawQuantityOfNodes:

    def __init__(self, dataframe, x, y):
        table_height = len(dataframe)
        table_breadth = len(dataframe.columns)
        self.nodes_quantity = DataFrame()

        # Проверяем что метка не в шапке
        if y == 0:
            raise Exception(f"Ключевое слово в первом столбце "
                            f"на строке {str(x + 2)}")

        if y + 1 >= table_breadth:
            raise Exception(
                "Не найдено количество для крайне правого узла"
            )

        #
        node_number = 1
        while (x + node_number < table_height) and (
                not isna(dataframe.iloc[x + node_number, y])):
            material = dataframe.iloc[x + node_number, y]
            number = dataframe.iloc[x + node_number, y + 1]

            # Проверяем корректность данных спецификации
            if isna(dataframe.iloc[x + node_number, y + 1]):
                raise Exception(
                    f"Для {material} отсутствует количество. "
                    "Метка на строке " +
                    f"{str(x + 2)} на столбце {str(y + 1)}"
                )
            if not isinstance(number, (float, int)):
                raise Exception(
                    f"Для {material}"
                    " количество не число. "
                    "Метка на строке "
                    f"{str(x + 2)} на столбце {str(y + 1)}"
                )
            # сдвиг координат связан с нумерацией с 0 и
            # с тем что первая строка уходит под шапку

            # Убираем пустоты с обеих сторон
            print(material)
            material.strip()
            self.nodes_quantity.loc[material, "quantity"] = number

            node_number += 1

        if node_number == 1:
            raise Exception(
                "Для группы узлов " +
                f"'{dataframe.iloc[x, y + 1]}' отсутствуют данные."
            )
