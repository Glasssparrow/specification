

def delete_nodes_without_quantity(quantity, regular_nodes, special_nodes):

    regular_nodes_keys = []
    for k in regular_nodes.keys():
        regular_nodes_keys.append(k)

    for k in regular_nodes_keys:
        if k not in quantity.keys():
            del regular_nodes[k]

    special_nodes_keys = []
    for k, v in special_nodes.items():
        special_nodes_keys.append(k)

    for k in special_nodes_keys:
        should_be_deleted = False
        for node_name in special_nodes[k].materials.keys():
            if node_name not in quantity.keys():
                should_be_deleted = True
        if should_be_deleted:
            del special_nodes[k]
