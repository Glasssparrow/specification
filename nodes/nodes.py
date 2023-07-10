from common.data_with_keywords import DataWithKeywords


def get_nodes(
        path, metadata, node_mark, ordered_list_mark, unordered_list_mark,
        extra_level_of_numeration_mark, subnode_mark
):

    sheet_list = []
    for index in metadata.index:
        if metadata.loc[index, "type"] == "nodes":
            sheet_list.append(index)

    for sheet_name in sheet_list:
        sheet = DataWithKeywords(
            path,
            sheet_name,
            [node_mark, ordered_list_mark, unordered_list_mark,
             extra_level_of_numeration_mark, subnode_mark],
            tolerate_key_not_found=True
        )

