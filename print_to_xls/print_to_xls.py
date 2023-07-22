from pandas import ExcelWriter


def print_to_xls(data, file_name, path, sheet_name):
    if path == "":
        with ExcelWriter(f"{file_name}.xlsx") as writer:
            data.to_excel(writer, sheet_name)
    else:
        with ExcelWriter(f"{path}/{file_name}.xlsx") as writer:
            data.to_excel(writer, sheet_name)
