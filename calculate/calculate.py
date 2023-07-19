

def get_materials_dict(quantity, regular_nodes, special_nodes):

    # Отбросил идею разметки особых узлов в данной функции.
    # Уровень оптимизации кода не важен, вычислительные мощности в избытке.
    materials_dict = {}

    # Заполняем материалы из обычных узлов
    for node_name, node in regular_nodes.items():
        if node_name not in quantity.keys():
            raise Exception(
                f"Не найдено количество для узла {node_name}"
            )
        for material, material_quantity in node.materials.items():
            materials_dict[material] = (
                material_quantity + materials_dict.get(material, 0)
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
    for special_node_name, special_node in special_nodes.items():
        for node_name, materials in special_node.materials.items():
            for material, material_quantity in materials.items():
                materials_dict[material] = (
                    material_quantity + materials_dict.get(material, 0)
                )

    return materials_dict


def get_dict_of_materials_for_special_nodes(
        quantity, special_nodes
):
    pass
