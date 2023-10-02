from pandas import DataFrame, isna
from math import ceil
from logging import info


def get_datasheet(dictionary, library):
    datasheet = DataFrame(columns=[
        "category_sort_priority", "subcategory_sort_priority",
        "sort_priority",

        "category", "subcategory",

        "position", "name", "description",
        "code", "manufacturer", "unit",
        "quantity", "mass", "comment",
    ])
    for k, v in dictionary.items():
        if isna(v):
            datasheet.loc[k, "quantity"] = v
        else:
            datasheet.loc[k, "quantity"] = ceil(v)
        if k in library.index:
            for column in [
                "category_sort_priority",
                "subcategory_sort_priority",
                "sort_priority",

                "category",
                "subcategory",

                "name",
                "description",
                "code",
                "manufacturer",
                "unit",
                "mass",
                "comment",
            ]:
                datasheet.loc[k, column] = (
                    library.loc[k, column]
                )
        else:
            info(f"{k} не найдено в библиотеке")
            for column in [
                "category_sort_priority",
                "subcategory_sort_priority",
                "sort_priority",
            ]:
                datasheet.loc[k, column] = 0
            datasheet.loc[k, "name"] = k
            datasheet.loc[k, "description"] = "Не найдено"

    datasheet = datasheet.sort_values(by=[
        "category_sort_priority",
        "subcategory_sort_priority",
        "sort_priority",
        "name",
    ])

    return datasheet


def get_specification(main, additional, library, library_metadata):
    specification = DataFrame(columns=[
        "category_sort_priority", "subcategory_sort_priority",
        "sort_priority",

        "category", "subcategory",

        "position", "name", "description",
        "code", "manufacturer", "unit",
        "quantity", "mass", "comment",
    ])

    main_specification = get_datasheet(main, library)
    additional_specifications = {}
    types_of_special_nodes = {}
    for special_node_name, special_node in additional.items():
        additional_specifications[special_node_name] = (
            get_datasheet(special_node, library)
        )
        types_of_special_nodes[special_node_name] = (
            special_node.type
        )

    # Проходимся по всем строкам основной части спецификации.
    # Создаем строку для каждой категории.
    # Если доходим до строки с особым узлом, добавляем все материалы из
    # этого особого узла.
    # Проставляем нумерация:
    # Каждая категория получает свой номер и каждый материал свой 2 номер.
    # Для unordered_list нумерацию получает только сам лист
    # Для ordered_list нумерацию получают только материалы
    # Для full_numeration нумерацию получают все элементы,
    # при этом материалы получают первые 2 номера как у листа, и
    # дополнительно свой 3 номер.
    category = "no category"
    category_name = "404 Not found"
    position_1_number = 0
    position_2_number = 0
    for index in main_specification.index:
        # Если новая категория, то добавляем строку с категорией.
        # В строку категории записывается имя категории из
        # метаданных библиотеки.
        if (
            not isna(main_specification.loc[index, "category"]) and
            main_specification.loc[index, "category"] != category
        ):

            category = main_specification.loc[index, "category"]

            for subcategory in library_metadata.data.index:
                if (
                    library_metadata.data.loc[
                        subcategory, "category"
                    ] == category
                ):
                    category_name = (
                        library_metadata.data.loc[subcategory,
                                                  "category_name"]
                    )
                    break
            specification.loc[category, "name"] = category_name
            # И нумерация
            position_1_number += 1
            position_2_number = 0
            specification.loc[category, "position"] = (
                f"{str(position_1_number)}."
            )
        # Заполняем данные для материала
        for column in [
            "category_sort_priority", "subcategory_sort_priority",
            "sort_priority",
            "category", "subcategory",
            "name", "description",
            "code", "manufacturer", "unit",
            "quantity", "mass", "comment",
        ]:
            specification.loc[index, column] = (
                main_specification.loc[index, column]
            )
        # Если это особый узел
        if index in types_of_special_nodes.keys():
            position_3_number = 0
            for material in additional_specifications[index].index:
                for column in [
                    "category_sort_priority", "subcategory_sort_priority",
                    "sort_priority",
                    "category", "subcategory",
                    "name", "description",
                    "code", "manufacturer", "unit",
                    "quantity", "mass", "comment",
                ]:
                    specification.loc[f"{index}.{material}",
                                      column] = (
                        additional_specifications[index].loc[
                            material, column
                        ]
                    )
                if types_of_special_nodes[index] == "ordered_list":
                    position_2_number += 1
                    specification.loc[f"{index}.{material}", "position"] = (
                        f"{position_1_number}.{position_2_number}"
                    )
                elif types_of_special_nodes[index] == "unordered_list":
                    pass
                elif types_of_special_nodes[index] == "full_numeration":
                    position_3_number += 1
                    specification.loc[f"{index}.{material}", "position"] = (
                        f"{position_1_number}.{position_2_number+1}."
                        f"{position_3_number}"
                    )
            if types_of_special_nodes[index] in [
                "full_numeration", "unordered_list"
            ]:
                position_2_number += 1
                specification.loc[index, "position"] = (
                    f"{position_1_number}.{position_2_number}"
                )
        # Нумерация если это не особый узел
        else:
            position_2_number += 1
            specification.loc[index, "position"] = (
                f"{position_1_number}.{position_2_number}"
            )

    return specification
