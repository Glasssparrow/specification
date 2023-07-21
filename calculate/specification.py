from pandas import DataFrame, isna
from math import ceil


def get_specification(main, additional, library):
    print(library.columns)
    specification = DataFrame(columns=[
        "category_sort_priority",
        "subcategory_sort_priority",
        "sort_priority",

        "position",
        "name",
        "description",
        "code",
        "manufacturer",
        "unit",
        "quantity",
        "mass",
        "comment",
    ]
    )
    for k, v in main.items():
        if isna(v):
            specification.loc[k, "quantity"] = v
        else:
            specification.loc[k, "quantity"] = ceil(v)
        if k in library.index:
            for column in [
                "category_sort_priority",
                "subcategory_sort_priority",
                "sort_priority",

                "name",
                "description",
                "code",
                "manufacturer",
                "unit",
                "mass",
                "comment",
            ]:
                specification.loc[k, column] = (
                    library.loc[k, column]
                )
        else:
            for column in [
                "category_sort_priority",
                "subcategory_sort_priority",
                "sort_priority",
            ]:
                specification.loc[k, column] = 0
