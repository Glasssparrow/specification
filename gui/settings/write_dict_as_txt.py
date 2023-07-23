

def write_to_txt_from_dict(path: str, dictionary, splitter=": ",
                           list_splitter=",", open_brackets="[",
                           close_bracket="]"):
    """
    Функция создающая текстовый файл из словаря в формате:
    "key"+"splitter"+"value".
    Путь принимается в формате folder/folder/file.txt
    """
    string = ""
    for k, v in dictionary.items():
        if isinstance(v, str):
            string += k + splitter + v + "\n"
        elif isinstance(v, list):
            string += k + splitter + open_brackets
            for value in v:
                if isinstance(v, str):
                    string += value + list_splitter
                else:
                    string += str(value) + list_splitter
            string = string[:-len(list_splitter)]
            string += close_bracket + "\n"
        elif type(v) == int or type(v) == float:
            string += k + splitter + str(v) + "\n"
        else:
            raise ValueError("Значение ни строка, ни лист, ни число")
    string = string[:-1]
    file = open(path, "w", encoding="utf-8")
    try:
        file.write(string)
    finally:
        file.close()
