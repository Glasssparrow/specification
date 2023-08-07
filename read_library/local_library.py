from common.raw_data import get_data_with_first_column_as_index
from pandas import isna


def edit_str(string):
    new_string = string.strip()
    return new_string.lower()


def add_local_library(
        library, nodes_metadata, library_metadata,
        default_priority, path,
        subcategory_column,
        priority_column, can_have_multiplier_column,
        name_column, description_column,
        code_column, manufacturer_column,
        unit_column, mass_column, comment_column
):
    sheet_list = []
    for index in nodes_metadata.index:
        if nodes_metadata.loc[index, "type"] == "library":
            sheet_list.append(index)

    for sheet_name in sheet_list:
        sheet = get_data_with_first_column_as_index(path, sheet_name)
        for index in sheet.index:
            index_for_library = edit_str(index)
            if (
                (sheet.loc[index, subcategory_column] not in
                 library_metadata.data.index) and
                not isna(sheet.loc[index, subcategory_column])
            ):
                raise Exception(
                    f"Не найдена категория "
                    f"{sheet.loc[index, subcategory_column]}"
                )
            # Записываем подкатегорию.
            if not isna(sheet.loc[index, subcategory_column]):
                library.loc[index_for_library, "subcategory"] = (
                    sheet.loc[index, subcategory_column]
                )
            else:
                library.loc[index_for_library, "subcategory"] = (
                    library_metadata.default_subcategory
                )
            # Вытаскиваем данные о подкатегории из метаданных.
            for column in [
                "category", "category_sort_priority",
                "subcategory_sort_priority"
            ]:
                library.loc[index_for_library, column] = (
                    library_metadata.data.loc[
                        library.loc[index_for_library, "subcategory"],
                        column
                    ]
                )
            # Колонка приоритета сортировки
            if not isna(sheet.loc[index, priority_column]):
                library.loc[index_for_library, "sort_priority"] = (
                    sheet.loc[index, priority_column]
                )
            else:
                library.loc[index_for_library, "sort_priority"] = default_priority
            # Колонка возможности наличия множителя
            if not isna(sheet.loc[index, can_have_multiplier_column]):
                library.loc[index_for_library, "can_have_multiplier"] = True
            else:
                library.loc[index_for_library, "can_have_multiplier"] = False

            for internal_column, specification_column in {
                "name": name_column,
                "description": description_column,
                "code": code_column,
                "manufacturer": manufacturer_column,
                "unit": unit_column,
                "mass": mass_column,
                "comment": comment_column
            }.items():
                library.loc[index_for_library, internal_column] = (
                    sheet.loc[index, specification_column]
                )
