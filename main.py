from read_metadata.library_meta import get_library_meta
from read_metadata.nodes_meta import get_nodes_meta
from read_library.main_library import get_library
from read_library.local_library import add_local_library
from nodes.quantity import get_nodes_quantity
from nodes.nodes import get_raw_nodes, get_nodes
from calculate.calculate import get_materials_dict, get_dict_of_materials_for_special_nodes
from calculate.specification import get_specification
from print_to_xls.print_to_xls import print_to_xls


def calculate_and_print_specification(
    specification_path,

    library_path,
    output_path,
    default_priority,
    output_setting_file_name,
    output_setting_sheet_name,

    library_setting_meta_list_name,
    library_setting_sheet_name_column,
    library_setting_subcategory_sort_priority_column,
    library_setting_is_default_subcategory_column,
    library_setting_category_column,
    library_setting_category_name_column,
    library_setting_category_sort_priority_column,
    library_setting_is_default_category_column,
    library_settings_priority_column,
    library_setting_can_have_multiplier_column,
    library_setting_name_column,
    library_setting_description_column,
    library_setting_code_column,
    library_setting_manufacturer_column,
    library_setting_unit_column,
    library_setting_mass_column,
    library_setting_comment_column,
    library_setting_subcategory_column,
    library_setting_priority_column,

    specification_setting_specification_meta_list_name,
    specification_setting_type_column,
    specification_setting_specification_keyword,
    specification_setting_nodes_keyword,
    specification_setting_library_keyword,
    specification_setting_node_mark,
    specification_setting_ordered_list_mark,
    specification_setting_unordered_list_mark,
    specification_setting_extra_level_of_numeration_mark,
    specification_setting_subnode_mark,
    specification_setting_quantity_mark,
):
    # Получаем данные о данных
    library_meta = get_library_meta(
        path=library_path,
        sheet_name=library_setting_meta_list_name,
        sheet_name_column=library_setting_sheet_name_column,
        subcategory_sort_priority_column=(
            library_setting_subcategory_sort_priority_column),
        is_default_subcategory_column=(
            library_setting_is_default_subcategory_column),
        category_column=library_setting_category_column,
        category_name_column=(
            library_setting_category_name_column),
        category_sort_priority_column=(
            library_setting_category_sort_priority_column),
        is_default_category_column=(
            library_setting_is_default_category_column),
        default_priority=default_priority
    )

    nodes_meta = get_nodes_meta(
        path=specification_path,
        sheet_name=specification_setting_specification_meta_list_name,
        type_column=specification_setting_type_column,
        specification_keyword=specification_setting_specification_keyword,
        nodes_keyword=specification_setting_nodes_keyword,
        library_keyword=specification_setting_library_keyword,
    )

    # Читаем библиотеку
    library = get_library(
        metadata=library_meta,
        default_priority=default_priority,
        priority_column=library_settings_priority_column,
        can_have_multiplier_column=(
            library_setting_can_have_multiplier_column),
        name_column=library_setting_name_column,
        description_column=library_setting_description_column,
        code_column=library_setting_code_column,
        manufacturer_column=library_setting_manufacturer_column,
        unit_column=library_setting_unit_column,
        mass_column=library_setting_mass_column,
        comment_column=library_setting_comment_column,
    )
    add_local_library(
        library=library,
        nodes_metadata=nodes_meta,
        library_metadata=library_meta,
        path=specification_path,
        default_priority=default_priority,
        subcategory_column=library_setting_subcategory_column,
        priority_column=library_setting_priority_column,
        can_have_multiplier_column=(
            library_setting_can_have_multiplier_column
        ),
        name_column=library_setting_name_column,
        description_column=library_setting_description_column,
        code_column=library_setting_code_column,
        manufacturer_column=library_setting_manufacturer_column,
        unit_column=library_setting_unit_column,
        mass_column=library_setting_mass_column,
        comment_column=library_setting_comment_column
    )

    # Читаем узлы
    nodes_list, ol_list, ul_list, num_list, subnodes_list = get_raw_nodes(
        path=specification_path,
        metadata=nodes_meta,
        node_mark=specification_setting_node_mark,
        ordered_list_mark=specification_setting_ordered_list_mark,
        unordered_list_mark=specification_setting_unordered_list_mark,
        extra_level_of_numeration_mark=(
            specification_setting_extra_level_of_numeration_mark
        ),
        subnode_mark=specification_setting_subnode_mark
    )

    regular_nodes, special_nodes = get_nodes(
        nodes_list, ol_list, ul_list, num_list, subnodes_list
    )

    nodes_quantity = get_nodes_quantity(
        path=specification_path,
        metadata=nodes_meta,
        quantity_mark=specification_setting_quantity_mark
    )

    # Формируем таблицу спецификации
    specification_table = get_materials_dict(
        nodes_quantity, regular_nodes, special_nodes
    )
    specification_extra = get_dict_of_materials_for_special_nodes(
        nodes_quantity, special_nodes
    )
    specification = get_specification(
        main=specification_table,
        additional=specification_extra,
        library=library,
        library_metadata=library_meta,
    )

    print_to_xls(
        data=specification,
        file_name=output_setting_file_name,
        path=output_path,
        sheet_name=output_setting_sheet_name,
    )
