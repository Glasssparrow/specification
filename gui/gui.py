from .settings.settings import return_settings_to_default
from .settings.read_txt_as_dict import read_as_dict
from tkinter import filedialog as fd
from tkinter import Button, Tk, Label


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
        pass

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

    def __init__(self):
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
