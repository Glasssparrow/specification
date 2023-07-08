from common.raw_data import get_data_with_first_column_as_index


def get_nodes_meta(path, sheet_name,
                   type_column, specification_keyword,
                   nodes_keyword, library_keyword):
    """
    Возвращает DataFrame с одним столбцом: "type".
    "specification" для спецификации.
    "nodes" для узлов.
    "library" для библиотеки.
    """
    data = get_data_with_first_column_as_index(path, sheet_name)
    for index in data.index:
        if data.loc[index, type_column] not in [
            specification_keyword,
            nodes_keyword,
            library_keyword
        ]:
            raise ValueError(f"Не верный тип листа данных "
                             f"{data.loc[index, type_column]}")
        for name_for_internal_use, source_data_name in {
            "specification": specification_keyword,
            "nodes": nodes_keyword,
            "library": library_keyword
        }.items():
            if data.loc[index, type_column] == source_data_name:
                data.loc[index, "type"] = name_for_internal_use
                continue
    data.pop(type_column)

    return data

