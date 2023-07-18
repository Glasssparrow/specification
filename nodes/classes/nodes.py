from pandas import isna, DataFrame


def edit_str(string):
    new_string = string.strip()
    return new_string.lower()


class RegularNode:

    def __init__(self, node):
        self.name = edit_str(node.name.lower())
        # На случай если понадобится разделить узлы
        # Пока не реализовано
        self.specification = "default"
        # Записываем материалы в словарь
        # Названия материалов строчными.
        self.materials = {}
        for index in node.materials.index:
            material_name = edit_str(index)
            if isna(node.materials.loc[index, "multiplier"]):
                self.materials[material_name] = (
                    node.materials.loc[index, "number"]
                )
            else:
                self.materials[material_name] = (
                    node.materials.loc[index, "number"] *
                    node.materials.loc[index, "multiplier"]
                )


class SpecialNode:

    def __init__(self, name, node_type):
        self.name = name
        # Тип особого узла
        self.type = node_type
        self.materials = {
            # "node_name": {}
        }
