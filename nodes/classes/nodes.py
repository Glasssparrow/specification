from pandas import isna, DataFrame


class RegularNode:

    def __init__(self):
        self.name = "name"
        # В случае необходимости разделить узлы
        self.specification = "default"
        self.materials = DataFrame()


class SpecialNode:

    def __init__(self):
        self.name = "name"
        # Тип особого узла
        self.type = "type"
        self.materials = {
            "node_name": DataFrame()
        }
