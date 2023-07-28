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

    # Формируем подузлы
    levels_list = []
    for node in subnodes_list:
        if node.material_name == "default":
            node.material_name = 0
        elif not isinstance(node.material_name, (int, float)):
            raise Exception(
                f"{node.name} имеет неправильную метку уровня подузла. "
                f"Метка подузла должна быть числом (или быть пуста)."
            )

        level = node.material_name
        if level not in levels_list:
            levels_list.append(level)

    levels_list.sort(reverse=True)

    subnodes = {}
    for node in subnodes_list:
        if node.name in subnodes.keys():
            raise Exception(f"{node.name} встречается дважды.")
        subnodes[node.name] = {}

    for number in levels_list:
        for node in subnodes_list:
            if node.material_name != number:
                continue

            data = node.materials

            for index in data.index:
                quantity = data.loc[index, "number"]
                if not isna(data.loc[index, "multiplier"]):
                    quantity *= data.loc[index, "multiplier"]
                if index in subnodes.keys():
                    for k, v in subnodes[index].items():
                        subnodes[node.name][k] = (
                            quantity * v +
                            subnodes[node.name].get(k, 0)
                        )
                else:
                    subnodes[node.name][index] = (
                        quantity +
                        subnodes[node.name].get(index, 0)
                    )

    for node_name, node in regular_nodes_dict.items():
        put_subnodes_into_dict(node.materials, subnodes, levels_list)
    for special_node_name, special_node in special_nodes_dict.items():
        for regular_node_name, dictionary in special_node.materials.items():
            put_subnodes_into_dict(dictionary, subnodes, levels_list)

    return regular_nodes_dict, special_nodes_dict


def put_subnodes_into_dict(dictionary, subnodes, levels_list):

    # Чтобы не идти сквозь словарь который меняем
    iterator = dictionary.copy()

    node_materials = dictionary
    for material_name, material_quantity in iterator.items():
        if material_name in subnodes.keys():
            del node_materials[material_name]
            for subnode_material, subnode_material_quantity in subnodes[
                material_name
            ].items():
                node_materials[subnode_material] = (
                    subnode_material_quantity * material_quantity +
                    node_materials.get(subnode_material, 0)
                )
