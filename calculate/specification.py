from pandas import DataFrame


def get_specification(main, additional, library):
    specification = DataFrame(columns=[
        "can_have_multiplier",
        "category_priority",
        "subcategory_priority",
        "priority",

        "name",
        "description",
        "code",
        "manufacturer",
        "unit",
        "mass",
        "comment",
    ]
    )
    for k, v in main.items():
        specification.loc[k, "quality"] = v
