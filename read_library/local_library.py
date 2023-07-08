from common.raw_data import get_data_with_first_column_as_index
from pandas import isna


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
            if (sheet.loc[index, subcategory_column] not in
                    library_metadata.data.index):
                raise Exception(
                    f"Не найдена категория "
                    f"{sheet.loc[index, subcategory_column]}"
                )
            # Записываем подкатегорию.
            library.loc[index, "subcategory"] = (
                sheet.loc[index, subcategory_column])
            # Вытаскиваем данные о подкатегории из метаданных.
            for column in [
                "category", "category_sort_priority",
                "subcategory_sort_priority"
            ]:
                library.loc[index, column] = (
                    library_metadata.data.loc[
                        sheet.loc[index, subcategory_column], column]
                )
            # Колонка приоритета сортировки
            if not isna(sheet.loc[index, priority_column]):
                library.loc[index, "sort_priority"] = (
                    sheet.loc[index, priority_column]
                )
            else:
                library.loc[index, "sort_priority"] = default_priority
            # Колонка возможности наличия множителя
            if not isna(sheet.loc[index, can_have_multiplier_column]):
                library.loc[index, "can_have_multiplier"] = True
            else:
                library.loc[index, "can_have_multiplier"] = False

            for internal_column, specification_column in {
                "name": name_column,
                "description": description_column,
                "code": code_column,
                "manufacturer": manufacturer_column,
                "unit": unit_column,
                "mass": mass_column,
                "comment": comment_column
            }.items():
                library.loc[index, internal_column] = (
                    sheet.loc[index, specification_column]
                )
