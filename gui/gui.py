from .settings.settings import return_settings_to_default
from .settings.read_txt_as_dict import read_as_dict
from tkinter import filedialog as fd
from tkinter import Button, Tk, Label
from datetime import datetime


class Gui:

    title_text = "Подсчет материалов 4.0"
    settings_label_text = "Сброс настроек закроет окно"

    # Функция нужна для формирования пути к папке из пути к файлу.
    @staticmethod
    def _cut_filename(path_to_file):
        """
        Обрабатывает путь к файлу в формате - ххх/ххх/file.file.
        Отсекает часть /file.file оставляя ххх/ххх
        """
        split = path_to_file.split("/")
        # Получаем длину последнего фрагмента после "/".
        # Прибавляем единицу т.к. "/" тоже убираем.
        delete = len(split[len(split)-1])+1
        return path_to_file[:-delete]

    # Функция выбора пути к файлу с исходными данными
    def _choose_filename(self):
        """
        Функция для кнопки выбора файла.
        Записывает в словарь settings путь к файлу и путь к папке.
        """
        self.input_path = (
            fd.askopenfilename(title="Выберите файл",
                               initialdir=(
                                   self.output_path)
                               )
        )
        self._text_path.configure(
            text=self.input_path
        )
        self.output_path = (
            self._cut_filename(self.input_path)
        )
        self._text_folder.configure(text=(
            self.output_path)
        )

    def _choose_folder(self):
        """
        Функция выбора папки в которую будет выводиться файл с выполненными
        расчетами.
        """
        self.output_path = (
            fd.askdirectory(title="Выберите папку",
                            initialdir=self.output_path)
        )
        self._text_folder.configure(text=self.output_path)

    def _correct_path(self):
        self._read_settings()
        self._text_path.configure(text=self.input_path)
        self._text_folder.configure(text=self.output_path)

    def _return_settings_to_default(self):
        return_settings_to_default()
        self._settings_window.destroy()
        self._correct_path()

    def _open_settings(self):
        self._settings_window = Tk()
        self._settings_window.title("Настройки")
        self._settings_window.geometry("230x50")

        self._return_to_default_button = (
            Button(self._settings_window, text="Вернуть настройки по умолчанию",
                   command=self._return_settings_to_default)
        )
        self._return_to_default_button.grid(column=0, row=1)

        self._warning_text = Label(self._settings_window,
                                   text=self.settings_label_text)
        self._warning_text.grid(column=0, row=0)

        self._settings_window.mainloop()

    def _calculate(self):
        try:
            self.calculate_and_print_specification(
                specification_path=self.input_path,
                library_path=(
                    self.settings_library["Путь к основной библиотеке"]
                ),
                output_path=self.output_path,
                default_priority=(
                    self.settings["Приоритет сортировки по умолчанию"]
                ),
                output_file_name=(
                    self.settings["Название итогового файла"]
                ),
                output_file_specification_sheet_name=(
                    self.settings[
                        "Название листа спецификации в итоговом файле"
                    ]
                ),
                library__meta_list_name=(
                    self.settings_library[
                        "Лист метаданных основной библиотеки"
                    ]
                ),
                library__sheet_name_column=(
                    self.settings_library[
                        "Столбец названий листов"
                    ]
                ),
                library__subcategory_sort_priority_column=(
                    self.settings_library[
                        "Столбец приоритета сортировки подкатегории"
                    ]
                ),
                library__is_default_subcategory_column=(
                    self.settings_library[
                        "Столбец метки подкатегории по умолчанию"
                    ]
                ),
                library__category_column=(
                    self.settings_library[
                        "Столбец категории"
                    ]
                ),
                library__category_name_column=(
                    self.settings_library[
                        "Столбец названия категории"
                    ]
                ),
                library__category_sort_priority_column=(
                    self.settings_library[
                        "Столбец приоритета сортировки категории"
                    ]
                ),
                library__is_default_category_column=(
                    self.settings_library[
                        "Столбец метки категории по умолчанию"
                    ]
                ),
                library__priority_column=(
                    self.settings_library[
                        "Столбец приоритета сортировки"
                    ]
                ),
                library__can_have_multiplier_column=(
                    self.settings_library[
                        "Столбец с меткой для материалов с множителем"
                    ]
                ),
                library__name_column=(
                    self.settings_library[
                        "Столбец наименования"
                    ]
                ),
                library__description_column=(
                    self.settings_library[
                        "Столбец обозначения"
                    ]
                ),
                library__code_column=(
                    self.settings_library[
                        "Столбец кода оборудования"
                    ]
                ),
                library__manufacturer_column=(
                    self.settings_library[
                        "Столбец производителя"
                    ]
                ),
                library__unit_column=(
                    self.settings_library[
                        "Столбец единицы измерения"
                    ]
                ),
                library__mass_column=(
                    self.settings_library[
                        "Столбец массы"
                    ]
                ),
                library__comment_column=(
                    self.settings_library[
                        "Столбец примечания"
                    ]
                ),
                library__subcategory_column=(
                    self.settings_library[
                        "Столбец подкатегории материала"
                    ]
                ),

                specification__specification_meta_list_name=(
                    self.settings_specification[
                        "Лист метаданных"
                    ]
                ),
                specification__type_column=(
                    self.settings_specification[
                        "Столбец с типами листов"
                    ]
                ),
                specification__specification_keyword=(
                    self.settings_specification[
                        "Ключевое слово для листов с количеством узлов"
                    ]
                ),
                keyword_sheet_for_nodes=(
                    self.settings_specification[
                        "Ключевое слово для листов с узлами"
                    ]
                ),
                keyword_sheet_for_library=(
                    self.settings_specification[
                        "Ключевое слово для листов с локальной библиотекой"
                    ]
                ),
                regular_node_mark=(
                    self.settings[
                        "Метка обычного узла"
                    ]
                ),
                ordered_list_mark=(
                    self.settings[
                        "Метка особого узла с нумерацией материалов"
                    ]
                ),
                unordered_list_mark=(
                    self.settings[
                        "Метка особого узла без нумерации материалов"
                    ]
                ),
                extra_level_of_numeration_mark=(
                    self.settings[
                        "Метка особого узла с дополнительным уровнем нумерации"
                    ]
                ),
                subnode_mark=(
                    self.settings[
                        "Метка подузла"
                    ]
                ),
                quantity_mark=(
                    self.settings[
                        "Метка количества узлов"
                    ]
                ),
            )
            time = datetime.now()

            text = ("Расчет выполнен успешно. Время " + str(time.hour) +
                    ":" + str(time.minute) + ":" + str(time.second) + "\n")
            self._text_warning.configure(text=text)
        except Exception as error:
            time = datetime.now()
            text = ("Расчет выполнен не был. Время " + str(time.hour) +
                    ":" + str(time.minute) + ":" + str(time.second) + "\n")
            for er in error.args:
                text += er + "\n"
            self._text_warning.configure(text=text)

    def _read_settings(self):
        """
        Считываем данные из текстовых файлов настрое
        """
        self.settings = read_as_dict(
            "settings/Основные настройки.txt"
        )
        self.settings_specification = read_as_dict(
            "settings/Настройки спецификации.txt"
        )
        self.settings_library = read_as_dict(
            "settings/Настройки библиотеки.txt"
        )
        self.input_path = "Путь ввод"
        self.output_path = self.settings["Путь по умолчанию"]

    def __init__(self, calculate_and_print_specification):
        self.calculate_and_print_specification = (
            calculate_and_print_specification
        )
        self._read_settings()
        # Оформление окна
        self._window = Tk()
        self._window.title(self.title_text)
        self._window.geometry("580x220")
        # Ширина для кнопок
        width = 12

        # Кнопка выбора файла
        self._file_selection_button = (
            Button(self._window, text="Выбрать файл исходных данных",
                   width=width * 3 + 3,
                   command=self._choose_filename,
                   bg="green")
        )
        self._file_selection_button.grid(columnspan=3, column=2,
                                         row=0)

        # Кнопка выбора папки
        self._folder_selection_button = (
            Button(self._window, text="Выбрать папку для печати",
                   width=width * 2 + 2,
                   command=self._choose_folder)
        )
        self._folder_selection_button.grid(columnspan=2, column=0,
                                           row=0)

        # Кнопка окна настроек
        self._settings_button = (
            Button(self._window, text="Настройки",
                   width=width,
                   command=self._open_settings))
        self._settings_button.grid(columnspan=1, column=5, row=0)

        # Текст пути к файлу
        self._text_path = (
            Label(text=self.input_path))
        self._text_path.grid(columnspan=6,
                             column=0, row=1)

        # Текст пути к папке в которую будем печатать
        self._text_folder = (
            Label(text=self.output_path))
        self._text_folder.grid(columnspan=6,
                               column=0, row=2)

        # Кнопка расчета
        self._calculate_button = (
            Button(self._window, text="Рассчитать",
                   width=width * 6 + 6,
                   command=self._calculate,
                   bg="green")
        )
        self._calculate_button.grid(columnspan=6, column=0,
                                    row=3)

        # Текст ошибки
        self._text_warning = (
            Label(text="Расчет еще не выполнялся"))
        self._text_warning.grid(columnspan=6,
                                column=0, row=4)

        # Запускаем окно
        self._window.mainloop()
