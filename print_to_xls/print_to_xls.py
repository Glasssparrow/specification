from pandas import ExcelWriter, DataFrame


def style(xls):
    def style_all(v, props=''):
        return props

    times_new_roman = 'font-family: "Times New Roman", Times, serif;'
    font_size = 'font-size:1em;'
    horizontal = 'text-align:center;'
    vertical = 'vertical-align:middle;'
    all_cells = (times_new_roman + font_size +
                 horizontal + vertical)
    not_all_cells = (times_new_roman + font_size +
                     vertical + 'text-align:left:')

    new_xls = xls.style\
        .applymap(style_all, props=all_cells)\
        .applymap(style_all, props=not_all_cells,
                  subset=["name", "comment", ])

    return new_xls


def print_to_xls(data, file_name, path, sheet_name):
    columns = ["position", "name", "description", "code", "manufacturer",
               "unit", "quantity", "mass", "comment", ]
    # Создаем таблицу
    specification = DataFrame(columns=columns)
    for index in data.index:
        for column in columns:
            specification.loc[index, column] = data.loc[index, column]
    # Накладываем стилизацию
    xls = style(specification)
    # Печатаем
    if path == "":  # Это для тестового расчета
        with ExcelWriter(f"{file_name}.xlsx") as writer:
            xls.to_excel(writer, sheet_name)
            data.to_excel(writer, "До обработки")
    else:
        with ExcelWriter(f"{path}/{file_name}.xlsx") as writer:
            xls.to_excel(writer, sheet_name)
            data.to_excel(writer, "До обработки")
