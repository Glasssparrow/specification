from common.data_with_keywords import DataWithKeywords
from .classes.raw_nodes import RawNode


def get_raw_nodes(
        path, metadata, node_mark, ordered_list_mark, unordered_list_mark,
        extra_level_of_numeration_mark, subnode_mark
):

    sheet_list = []
    for index in metadata.index:
        if metadata.loc[index, "type"] == "nodes":
            sheet_list.append(index)

    nodes_list = []
    ol_list = []
    ul_list = []
    num_list = []
    subnodes_list = []

    for sheet_name in sheet_list:
        sheet = DataWithKeywords(
            path,
            sheet_name,
            [node_mark, ordered_list_mark, unordered_list_mark,
             extra_level_of_numeration_mark, subnode_mark],
            tolerate_key_not_found=True
        )
        for keyword, data_list in {
            node_mark: nodes_list,
            ordered_list_mark: ol_list,
            unordered_list_mark: ul_list,
            extra_level_of_numeration_mark: num_list,
            subnode_mark: subnodes_list,
        }.items():
            for coord in sheet.keys[keyword]:
                data_list.append(RawNode(sheet.data, coord[0], coord[1]))

    return nodes_list, ol_list, ul_list, num_list, subnodes_list


def get_nodes(nodes_list, ol_list, ul_list, num_list, subnodes_list):
    pass
