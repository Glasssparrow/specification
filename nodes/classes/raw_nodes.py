from pandas import isna, NA, DataFrame


class RawNode:

    def __init__(self, dataframe, x, y):
        table_height = len(dataframe)
        table_breadth = len(dataframe.columns)
        self.materials = DataFrame()

        # Проверяем положение метки, название узла
        if isna(dataframe.iloc[x - 1, y - 1]):
            raise Exception(
                f"Нет названия узла. Метка на строке "
                f"{str(x + 2)} на столбце {str(y + 1)}"
            )
        if not isinstance(dataframe.iloc[x - 1, y - 1], (str, float, int)):
            raise Exception(
                f"Название узла должно быть строкой "
                f"или числом. Метка на строке {str(x + 2)} "
                f"на столбце {str(y + 1)}"
            )
        if y == 0:
            raise Exception(f"Ключевое слово в первом столбце "
                            f"на строке {str(x + 2)}")

        # Записываем имя узла.
        self.name = dataframe.iloc[x - 1, y - 1]

        # Проверяем категории узла
        if (
                not isna(dataframe.iloc[x, y - 1]) and
                not isinstance(dataframe.iloc[x, y - 1], str)
        ):
            raise Exception(
                "Ячейка категорий узла должна содержать"
                " строку или быть пустой "
                f"Ошибка возникла в узле {self.name}"
                " Метка на строке " +
                f"{str(x + 2)} на столбце {str(y + 1)}"
            )

        # Записываем категории для узла
        if isna(dataframe.iloc[x, y - 1]):
            self.material_name = "default"
        else:
            self.material_name = dataframe.iloc[x, y - 1]

        # Начинаем цикл через спецификацию
        node_material_number = 1
        while (x + node_material_number < table_height) and (
                not isna(dataframe.iloc[x + node_material_number, y - 1])):
            material = dataframe.iloc[x + node_material_number, y - 1]
            number = dataframe.iloc[x + node_material_number, y]
            if y + 1 < table_breadth:
                if isna(dataframe.iloc[x + node_material_number, y + 1]):
                    multiplier = NA
                else:
                    multiplier = dataframe.iloc[x+node_material_number, y+1]
            else:
                multiplier = NA

            # Проверяем корректность данных спецификации
            if isna(dataframe.iloc[x + node_material_number, y]):
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
            if not isna(multiplier) and (
                    not isinstance(multiplier, (float, int))
            ):
                raise Exception(
                    f"Для {material}"
                    " множитель не число и не пустая ячейка. "
                    "Метка на строке "
                    f"{str(x + 2)} на столбце {str(y + 1)}"
                )

            # Убираем пустоты с обеих сторон
            material.strip()
            self.materials.loc[material, "number"] = number
            self.materials.loc[material, "multiplier"] = multiplier

            node_material_number += 1

        if node_material_number == 1:
            raise Exception(
                "Спецификация узла " +
                f"{dataframe.iloc[x - 1, y - 1]} пуста."
            )
