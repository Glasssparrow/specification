from common.raw_data import get_data_with_first_column_as_index
from pandas import DataFrame, isna


def get_library(metadata, default_priority,
                priority_column, can_have_multiplier_column,
                name_column, description_column,
                code_column, manufacturer_column,
                unit_column, mass_column, comment_column):
    lib = DataFrame()
    for subcategory in metadata.data.index:
        sheet = get_data_with_first_column_as_index(
            metadata.path, metadata.data.loc[subcategory, "sheet_name"]
        )
        for index in sheet.index:
            if index in lib.index:
                raise Exception(
                    f"Материал {index} занесен в основную библиотеку "
                    f"дважды."
                )
            lib.loc[index, "category"] = (
                metadata.data.loc[subcategory, "category"]
            )
            lib.loc[index, "subcategory"] = subcategory
            lib.loc[index, "category_sort_priority"] = (
                metadata.data.loc[subcategory, "category_sort_priority"]
            )
            lib.loc[index, "subcategory_sort_priority"] = (
                metadata.data.loc[subcategory, "subcategory_sort_priority"]
            )
            if not isna(sheet.loc[index, priority_column]):
                lib.loc[index, "sort_priority"] = (
                    sheet.loc[index, priority_column]
                )
            else:
                lib.loc[index, "sort_priority"] = default_priority
            if not isna(sheet.loc[index, can_have_multiplier_column]):
                lib.loc[index, "can_have_multiplier"] = True
            else:
                lib.loc[index, "can_have_multiplier"] = False
            for internal_name, source_data_name in {
                "name": name_column,
                "description": description_column,
                "code": code_column,
                "manufacturer": manufacturer_column,
                "unit": unit_column,
                "mass": mass_column,
                "comment": comment_column
            }.items():
                lib.loc[index, internal_name] = (
                    sheet.loc[index, source_data_name]
                )

    return lib
