from common.data_with_keywords import DataWithKeywords
from .classes.raw_quantity import RawQuantityOfNodes


def get_nodes_quantity(path, metadata, quantity_mark):

    sheet_list = []
    for index in metadata.index:
        if metadata.loc[index, "type"] == "specification":
            sheet_list.append(index)

    nodes_quantity_list = []
    nodes_quantity = {}

    for sheet_name in sheet_list:
        sheet = DataWithKeywords(
            path,
            sheet_name,
            [quantity_mark],
            tolerate_key_not_found=False
        )

        for v in sheet.keys[quantity_mark]:
            nodes_quantity_list.append(
                RawQuantityOfNodes(sheet.data, v[0], v[1])
            )
    for element in nodes_quantity_list:
        for index in element.nodes_quantity.index:
            nodes_quantity[index] = (
                element.nodes_quantity.loc[index, "quantity"] +
                nodes_quantity.get(index, 0)
                                    )

    return nodes_quantity
