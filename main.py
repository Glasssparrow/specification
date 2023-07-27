from read_metadata.library_meta import get_library_meta
from read_metadata.nodes_meta import get_nodes_meta
from read_library.main_library import get_library
from read_library.local_library import add_local_library
from nodes.quantity import get_nodes_quantity
from nodes.nodes import get_raw_nodes, get_nodes
from nodes.check_multiplier import check_multiplier
from calculate.calculate import get_materials_dict, get_dict_of_materials_for_special_nodes
from calculate.specification import get_specification
from print_to_xls.print_to_xls import print_to_xls


def calculate_and_print_specification(
    specification_path,

    library_path,
    output_path,
    default_priority,
    output_file_name,
    output_file_specification_sheet_name,

    library__meta_list_name,
    library__sheet_name_column,
    library__subcategory_sort_priority_column,
    library__is_default_subcategory_column,
    library__category_column,
    library__category_name_column,
    library__category_sort_priority_column,
    library__is_default_category_column,
    library__priority_column,
    library__can_have_multiplier_column,
    library__name_column,
    library__description_column,
    library__code_column,
    library__manufacturer_column,
    library__unit_column,
    library__mass_column,
    library__comment_column,
    library__subcategory_column,

    specification__specification_meta_list_name,
    specification__type_column,
    specification__specification_keyword,
    keyword_sheet_for_nodes,
    keyword_sheet_for_library,
    regular_node_mark,
    ordered_list_mark,
    unordered_list_mark,
    extra_level_of_numeration_mark,
    subnode_mark,
    quantity_mark,
):
    # Получаем данные о данных
    library_meta = get_library_meta(
        path=library_path,
        sheet_name=library__meta_list_name,
        sheet_name_column=library__sheet_name_column,
        subcategory_sort_priority_column=(
            library__subcategory_sort_priority_column),
        is_default_subcategory_column=(
            library__is_default_subcategory_column),
        category_column=library__category_column,
        category_name_column=(
            library__category_name_column),
        category_sort_priority_column=(
            library__category_sort_priority_column),
        is_default_category_column=(
            library__is_default_category_column),
        default_priority=default_priority
    )

    nodes_meta = get_nodes_meta(
        path=specification_path,
        sheet_name=specification__specification_meta_list_name,
        type_column=specification__type_column,
        specification_keyword=specification__specification_keyword,
        nodes_keyword=keyword_sheet_for_nodes,
        library_keyword=keyword_sheet_for_library,
    )

    # Читаем библиотеку
    library = get_library(
        metadata=library_meta,
        default_priority=default_priority,
        priority_column=library__priority_column,
        can_have_multiplier_column=(
            library__can_have_multiplier_column),
        name_column=library__name_column,
        description_column=library__description_column,
        code_column=library__code_column,
        manufacturer_column=library__manufacturer_column,
        unit_column=library__unit_column,
        mass_column=library__mass_column,
        comment_column=library__comment_column,
    )
    add_local_library(
        library=library,
        nodes_metadata=nodes_meta,
        library_metadata=library_meta,
        path=specification_path,
        default_priority=default_priority,
        subcategory_column=library__subcategory_column,
        priority_column=library__priority_column,
        can_have_multiplier_column=(
            library__can_have_multiplier_column
        ),
        name_column=library__name_column,
        description_column=library__description_column,
        code_column=library__code_column,
        manufacturer_column=library__manufacturer_column,
        unit_column=library__unit_column,
        mass_column=library__mass_column,
        comment_column=library__comment_column
    )

    # Читаем узлы
    nodes_list, ol_list, ul_list, num_list, subnodes_list = get_raw_nodes(
        path=specification_path,
        metadata=nodes_meta,
        node_mark=regular_node_mark,
        ordered_list_mark=ordered_list_mark,
        unordered_list_mark=unordered_list_mark,
        extra_level_of_numeration_mark=(
            extra_level_of_numeration_mark
        ),
        subnode_mark=subnode_mark
    )

    # Проверяем что множитель есть только у материалов с соответствующей
    # меткой в библиотеке.
    check_multiplier(
        nodes_list, ol_list, ul_list, num_list, subnodes_list, library
    )

    regular_nodes, special_nodes = get_nodes(
        nodes_list, ol_list, ul_list, num_list, subnodes_list
    )

    nodes_quantity = get_nodes_quantity(
        path=specification_path,
        metadata=nodes_meta,
        quantity_mark=quantity_mark
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
        file_name=output_file_name,
        path=output_path,
        sheet_name=output_file_specification_sheet_name,
    )
