from common.raw_data import get_data_with_first_column_as_index
from pandas import isna, DataFrame


class LibraryMeta:

    def __init__(self):
        self.data = DataFrame()


def get_library_meta(path, sheet_name,
                     default_priority,
                     sheet_name_column, subcategory_sort_priority_column,
                     is_default_subcategory_column, category_column,
                     category_name_column, category_sort_priority_column,
                     is_default_category_column):
    data = get_data_with_first_column_as_index(path, sheet_name)
    meta = LibraryMeta()
    tmp = {
        "sheet_name": "не выбрано",
        "category": "не выбрано",
        "category_name": "не выбрано"
    }
    default_subcategory = "404 Not found"
    default_category = "404 Not found"
    # Переносим таблицу заполняя пустоты и используя
    # названия столбцов которые далее будут применяться в программе.
    for index in data.index:
        for name_for_internal_use, source_data_name in {
            "sheet_name": sheet_name_column,
            "category": category_column,
            "category_name": category_name_column
        }.items():
            if not isna(data.loc[index, source_data_name]):
                meta.data.loc[index, name_for_internal_use] = (
                    data.loc[index, source_data_name])
                tmp[name_for_internal_use] = (
                    data.loc[index, source_data_name])
            else:
                meta.data.loc[index, name_for_internal_use] = (
                    tmp[name_for_internal_use])
        for name_for_internal_use, source_data_name in {
            "subcategory_sort_priority": subcategory_sort_priority_column,
            "category_sort_priority": category_sort_priority_column
        }.items():
            if not isna(data.loc[index, source_data_name]):
                meta.data.loc[index, name_for_internal_use] = (
                    data.loc[index, source_data_name])
            else:
                meta.data.loc[index, name_for_internal_use] = (
                    default_priority)
        if not isna(data.loc[index, is_default_subcategory_column]):
            meta.default_subcategory = (
                data.loc[index, is_default_subcategory_column])
        if not isna(data.loc[index, is_default_category_column]):
            meta.default_subcategory = (
                data.loc[index, is_default_category_column])
    return meta