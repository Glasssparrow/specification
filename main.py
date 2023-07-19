from read_metadata.library_meta import get_library_meta
from read_metadata.nodes_meta import get_nodes_meta
from read_library.main_library import get_library
from read_library.local_library import add_local_library
from nodes.quantity import get_nodes_quantity
from nodes.nodes import get_raw_nodes, get_nodes
from calculate.calculate import get_materials_dict, get_dict_of_materials_for_special_nodes
from calculate.specification import get_specification
from print_to_xls.print_to_xls import print_to_xls


# Эти данные должны подгружаться из настроек
main_settings = {
    "default_priority": 3
}

library_settings = {
    # Данные о местонахождении метаданных
    "library_path": "Library.xlsx",
    "library_meta_list_name": "Категории",

    # Данные для чтения метаданных
    "sheet_name_column": "Sheet name",
    "subcategory_sort_priority_column": "Sort priority",
    "is_default_subcategory_column": "Is default subcategory",
    "category_column": "Category",
    "category_name_column": "Category name",
    "category_sort_priority_column": "Category priority",
    "is_default_category_column": "Is default category",

    # Данные для чтения библиотеки
    "priority_column": "Приоритет",
    "can_have_multiplier_column": "Есть множитель",
    "name_column": "Наименование",
    "description_column": "Обозначение",
    "code_column": "Код",
    "manufacturer_column": "Производитель",
    "unit_column": "Единица измерения",
    "mass_column": "Масса",
    "comment_column": "Примечание",

    # Колонка уникальная для локальной библиотеки
    "subcategory_column": "Категория",
}

specification_settings = {
    "specification_meta_list_name": "Метаданные",

    "type_column": "Тип",
    "specification_keyword": "спецификация",
    "nodes_keyword": "узлы",
    "library_keyword": "библиотека",

    "node_mark": "node",
    "ordered_list_mark": "ol",
    "unordered_list_mark": "ul",
    "extra_level_of_numeration_mark": "num",
    "subnode_mark": "subnode",
    "quantity_mark": "KEY"
}

# Этот путь должен быть получен от графического интерфейса
specification_path = "tests/123.xlsx"

# Получаем данные о данных
library_meta = get_library_meta(
    path=library_settings["library_path"],
    sheet_name=library_settings["library_meta_list_name"],
    sheet_name_column=library_settings["sheet_name_column"],
    subcategory_sort_priority_column=(
        library_settings["subcategory_sort_priority_column"]),
    is_default_subcategory_column=(
        library_settings["is_default_subcategory_column"]),
    category_column=library_settings["category_column"],
    category_name_column=(
        library_settings["category_name_column"]),
    category_sort_priority_column=(
        library_settings["category_sort_priority_column"]),
    is_default_category_column=(
        library_settings["is_default_category_column"]),
    default_priority=(
        main_settings["default_priority"]))

nodes_meta = get_nodes_meta(
    specification_path,
    specification_settings["specification_meta_list_name"],
    specification_settings["type_column"],
    specification_settings["specification_keyword"],
    specification_settings["nodes_keyword"],
    specification_settings["library_keyword"]
)

# Читаем библиотеку
library = get_library(
    metadata=library_meta,
    default_priority=main_settings["default_priority"],
    priority_column=library_settings["priority_column"],
    can_have_multiplier_column=library_settings[
        "can_have_multiplier_column"],
    name_column=library_settings["name_column"],
    description_column=library_settings["description_column"],
    code_column=library_settings["code_column"],
    manufacturer_column=library_settings["manufacturer_column"],
    unit_column=library_settings["unit_column"],
    mass_column=library_settings["mass_column"],
    comment_column=library_settings["comment_column"]
)
add_local_library(
    library=library,
    nodes_metadata=nodes_meta,
    library_metadata=library_meta,
    path=specification_path,
    default_priority=main_settings["default_priority"],
    subcategory_column=library_settings["subcategory_column"],
    priority_column=library_settings["priority_column"],
    can_have_multiplier_column=library_settings[
        "can_have_multiplier_column"],
    name_column=library_settings["name_column"],
    description_column=library_settings["description_column"],
    code_column=library_settings["code_column"],
    manufacturer_column=library_settings["manufacturer_column"],
    unit_column=library_settings["unit_column"],
    mass_column=library_settings["mass_column"],
    comment_column=library_settings["comment_column"]
)

# Читаем узлы
nodes_list, ol_list, ul_list, num_list, subnodes_list = get_raw_nodes(
    path=specification_path,
    metadata=nodes_meta,
    node_mark=specification_settings["node_mark"],
    ordered_list_mark=specification_settings["ordered_list_mark"],
    unordered_list_mark=specification_settings["unordered_list_mark"],
    extra_level_of_numeration_mark=specification_settings[
        "extra_level_of_numeration_mark"
    ],
    subnode_mark=specification_settings["subnode_mark"]
)

regular_nodes, special_nodes = get_nodes(
    nodes_list, ol_list, ul_list, num_list, subnodes_list
)

nodes_quantity = get_nodes_quantity(
    path=specification_path,
    metadata=nodes_meta,
    quantity_mark=specification_settings["quantity_mark"]
)


# Формируем таблицу спецификации
specification_table = get_materials_dict(
    nodes_quantity, regular_nodes, special_nodes
)
specification_extra = get_dict_of_materials_for_special_nodes(
    nodes_quantity, special_nodes
)
specification = get_specification(
    specification_table, specification_extra, library
)

print_to_xls(specification)
