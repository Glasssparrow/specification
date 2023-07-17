from common.data_with_keywords import DataWithKeywords
from .classes.raw_nodes import RawNode
from .classes.nodes import RegularNode, SpecialNode


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
    for tmp_nodes_list in [
        nodes_list,
        ol_list,
        ul_list,
        num_list,
        subnodes_list,
    ]:
        in_the_list = []
        for node in tmp_nodes_list:
            if node.name in in_the_list:
                raise Exception(
                    f"Два узла {node.name} одного типа"
                )
            in_the_list.append(node.name)

    return nodes_list, ol_list, ul_list, num_list, subnodes_list


def get_nodes(nodes_list, ol_list, ul_list, num_list, subnodes_list):
    regular_nodes_dict = {}
    for node in nodes_list:
        new_node = RegularNode(node)
        if new_node.name in regular_nodes_dict.keys():
            raise Exception(
                f"Узел {new_node.name} встречается дважды"
            )
        regular_nodes_dict[new_node.name] = new_node

    # Создаем экземпляры и проверяем что нет двух узлов
    # с разным типом, но одинаковым именем.
    for current_list in [ol_list, ul_list, num_list]:
        for node in current_list:
            pass
