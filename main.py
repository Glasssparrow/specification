from read_metadata.library_meta import get_library_meta
from read_metadata.nodes_meta import get_nodes_meta
from read_library.main_library import get_library
from read_library.local_library import add_local_library
from nodes.quantity import get_nodes_quantity
from nodes.nodes import get_nodes
from calculate.calculate import get_specification_table, get_specification_extra
from calculate.specification import get_specification
from print_to_xls.print_to_xls import print_to_xls


# Эти данные должны подгружаться из настроек
library_path = "Library.xlsx"
library_meta_list_name = "Категории"
specification_meta_list_name = "Метаданные"

# Этот путь должен быть получен от графического интерфейса
specification_path = "tests/123.xlsx"

# Получаем данные о данных
library_meta = get_library_meta(library_path, library_meta_list_name)
nodes_meta = get_nodes_meta(specification_path,
                            specification_meta_list_name)

# Читаем библиотеку
library = get_library(library_meta)
add_local_library(library, nodes_meta)

# Читаем узлы
nodes_quantity = get_nodes_quantity(nodes_meta)
nodes = get_nodes(nodes_meta)

# Формируем таблицу спецификации
specification_table = get_specification_table(nodes_quantity,
                                              nodes)
specification_extra = get_specification_extra(nodes_quantity,
                                              nodes)
specification = get_specification(specification_table, specification_extra,
                                  library)

print_to_xls(specification)
