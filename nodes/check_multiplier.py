from pandas import isna
from logging import info


def check_multiplier(
    nodes_list, ol_list, ul_list, num_list, subnodes_list, library
):
    names_of_subnodes = []
    for subnode in subnodes_list:
        names_of_subnodes.append(subnode.name)
    for current_list in [
        nodes_list, ol_list, ul_list, num_list, subnodes_list
    ]:
        for current_node in current_list:
            for index in current_node.materials.index:
                materials = current_node.materials
                material = index.strip().lower()
                if material not in library.index:
                    pass
                else:
                    if library.loc[material, "can_have_multiplier"]:
                        if isna(materials.loc[index, "multiplier"]):
                            info(f"{material} в узле {current_node.name}"
                                 f" не должен иметь множителя.")
                    else:
                        if not isna(
                            materials.loc[index, "multiplier"]
                        ):
                            info(f"{material} в узле {current_node.name}"
                                 f" должен иметь множитель.")

