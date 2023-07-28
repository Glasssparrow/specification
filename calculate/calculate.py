from pandas import NA
from .classes.results import SpecialNodeFinal


def get_materials_dict(quantity, regular_nodes, special_nodes):

    materials_dict = {}

    nodes_from_quantity_for_special_nodes = []
    for v in special_nodes.values():
        for x in v.materials.keys():
            nodes_from_quantity_for_special_nodes.append(x)
    for node_name in quantity.keys():
        if (
            node_name not in regular_nodes.keys() and
            node_name not in nodes_from_quantity_for_special_nodes
        ):
            raise Exception(
                f"Не найден узел {node_name}"
            )

    # Заполняем материалы из обычных узлов
    for node_name, node in regular_nodes.items():
        if node_name not in quantity.keys():
            raise Exception(
                f"Не найдено количество для узла {node_name}"
            )
        for material, material_quantity in node.materials.items():
            materials_dict[material] = (
                material_quantity * quantity[node_name]
                + materials_dict.get(material, 0)
            )

    # Поднимаем ошибку если обычный узел включает в себя особый
    for node_name, node in special_nodes.items():
        if node_name in materials_dict.keys():
            raise Exception(
                f"Материал {node_name} не может быть одновременно "
                f"особым узлом типа {node.type} и одним из материалов "
                f"в составе обычного узла."
            )

    # Добавляем особые узлы в словарь
    # NA это как раз метка особого узлы
    for special_node_name in special_nodes.keys():
        materials_dict[special_node_name] = NA

    return materials_dict


def get_dict_of_materials_for_special_nodes(
        quantity, special_nodes
):
    materials_dict = {}
    # Проходимся по всем особым узлам из исходных данных.
    # Каждый узел это словарь с парой дополнительных атрибутов.
    # Записываем для каждого особого узла его тип.
    # Затем проходим по словарю материалов из исходного узла,
    # записываем количество материалов с учетом количества узлов
    # в новый узел.
    for special_node_name, special_node in special_nodes.items():
        materials_dict[special_node_name] = SpecialNodeFinal()
        materials_dict[special_node_name].type = special_node.type
        for node_name, node_dict in special_node.materials.items():
            if node_name not in quantity.keys():
                raise Exception(
                    f"Не найден узел {node_name}"
                )
            materials_dict[special_node_name].quantity += quantity[node_name]
            for material, material_quantity in node_dict.items():
                materials_dict[special_node_name][material] = (
                    material_quantity * quantity[node_name] +
                    materials_dict[special_node_name].get(material, 0)
                )

    return materials_dict
