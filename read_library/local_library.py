

def add_local_library(
        library, nodes_metadata, library_metadata,
        default_priority,
        subcategory_column,
        priority_column, can_have_multiplier_column,
        name_column, description_column,
        code_column, manufacturer_column,
        unit_column, mass_column, comment_column
):
    sheet_list = []
    for index in nodes_metadata.index:
        if nodes_metadata.loc[index, "type"] == "specification":
            sheet_list.append(index)

    for sheet in sheet_list:
        pass
