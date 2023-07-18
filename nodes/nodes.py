from common.data_with_keywords import DataWithKeywords
from .classes.raw_nodes import RawNode
from .classes.nodes import RegularNode, SpecialNode, edit_str
from pandas import isna


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

    special_nodes_dict = {}
    # Создаем экземпляры и проверяем что нет двух узлов
    # с разным типом, но одинаковым именем.
    for current_type, current_list in {
        "ordered_list": ol_list,
        "unordered_list": ul_list,
        "full_numeration": num_list,
    }.items():
        for node in current_list:
            # Именем нового узла будет тип материала из необработанного узла
            node_name = edit_str(node.material_name)
            if (
                node_name in special_nodes_dict.keys() and
                special_nodes_dict[node_name].type != current_type
            ):
                raise Exception(
                    f"{node_name} имеет два разных типа, что недопустимо."
                )
            special_nodes_dict[node_name] = (
                SpecialNode(name=node_name, node_type=current_type)
            )
            materials_dict = {}
            for index in node.materials.index:
                material_name = edit_str(index)
                if isna(node.materials.loc[index, "multiplier"]):
                    materials_dict[material_name] = (
                        node.materials.loc[index, "number"]
                    )
                else:
                    materials_dict[material_name] = (
                            node.materials.loc[index, "number"] *
                            node.materials.loc[index, "multiplier"]
                    )
            special_nodes_dict[node_name].materials[edit_str(node.name)] = (
                materials_dict
            )
    return regular_nodes_dict, special_nodes_dict
