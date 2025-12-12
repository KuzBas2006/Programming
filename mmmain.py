import sys
import os
import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

# Добавляем путь к Qt plugins
os.environ['QT_QPA_PATFORM_PLUGIN_PATH'] = ''

# НАСТРОЙКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ

DB_HOST = "127.0.0.1"  # Адрес сервера
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "997755"


def execute_sql_command(sql_command):
    """
    Функция для выполнения SQL-запросов к базе данных
    """
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()

        # Выполняем SQL-запрос
        cur.execute(sql_command)

        # Пытаемся получить результаты (если запрос их возвращает)
        try:
            results = cur.fetchall()  # Для SELECT запросов
        except psycopg2.ProgrammingError:
            # Это нормально для команд INSERT, UPDATE, DELETE
            conn.commit()  # Подтверждаем изменения
            results = None
        except Exception as e:
            conn.rollback()  # Откатываем изменения при ошибке
            raise e
        else:
            conn.commit()  # Подтверждаем изменения

        # Закрываем соединение
        cur.close()
        conn.close()

        return results if results else []
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        raise e


class EditRecordDialog(QtWidgets.QDialog):
    """Диалоговое окно для редактирования/добавления записей в основную таблицу"""

    def __init__(self, parent=None, record_info=None):
        super().__init__(parent)
        self.record_info = record_info
        self.setWindowTitle("Редактировать запись" if record_info else "Новая запись")
        self.setModal(True)
        self.setup_interface()

    def setup_interface(self):
        """Создание интерфейса окна"""
        layout = QtWidgets.QVBoxLayout(self)

        # Форма с полями ввода
        form_layout = QtWidgets.QFormLayout()

        # Создаем поля ввода для каждого атрибута
        self.surname_input = QtWidgets.QLineEdit()
        form_layout.addRow("Фамилия:", self.surname_input)

        self.firstname_input = QtWidgets.QLineEdit()
        form_layout.addRow("Имя:", self.firstname_input)

        self.patronymic_input = QtWidgets.QLineEdit()
        form_layout.addRow("Отчество:", self.patronymic_input)

        self.street_input = QtWidgets.QLineEdit()
        form_layout.addRow("Улица:", self.street_input)

        self.house_input = QtWidgets.QLineEdit()
        form_layout.addRow("Дом:", self.house_input)

        self.housing_input = QtWidgets.QLineEdit()
        form_layout.addRow("Корпус:", self.housing_input)

        self.apartment_input = QtWidgets.QLineEdit()
        form_layout.addRow("Квартира:", self.apartment_input)

        self.phone_input = QtWidgets.QLineEdit()
        form_layout.addRow("Телефон:", self.phone_input)

        layout.addLayout(form_layout)

        # Если редактируем существующую запись - заполняем поля
        if self.record_info:
            self.surname_input.setText(self.record_info[1])
            self.firstname_input.setText(self.record_info[2])
            self.patronymic_input.setText(self.record_info[3])
            self.street_input.setText(self.record_info[4])
            self.house_input.setText(str(self.record_info[5]))
            self.housing_input.setText(str(self.record_info[6] or ''))
            self.apartment_input.setText(str(self.record_info[7] or ''))
            self.phone_input.setText(self.record_info[8] or '')

        # Кнопки действий
        buttons_layout = QtWidgets.QHBoxLayout()
        button_text = "Сохранить" if self.record_info else "Создать"
        self.confirm_button = QtWidgets.QPushButton(button_text)
        self.confirm_button.clicked.connect(self.accept)
        self.abort_button = QtWidgets.QPushButton("Отмена")
        self.abort_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.confirm_button)
        buttons_layout.addWidget(self.abort_button)
        layout.addLayout(buttons_layout)

    def collect_data(self):
        """Сбор данных из полей ввода"""
        return {
            'surname': self.surname_input.text().strip(),
            'firstname': self.firstname_input.text().strip(),
            'patronymic': self.patronymic_input.text().strip(),
            'street': self.street_input.text().strip(),
            'house': self.house_input.text().strip(),
            'housing': self.housing_input.text().strip(),
            'apartment': self.apartment_input.text().strip(),
            'phone': self.phone_input.text().strip()
        }


class EditReferenceDialog(QtWidgets.QDialog):
    """Диалоговое окно для редактирования справочных таблиц"""

    def __init__(self, parent=None, record_info=None, reference_table=""):
        super().__init__(parent)
        self.record_info = record_info
        self.reference_table = reference_table
        self.setWindowTitle(f"Редактировать {reference_table}" if record_info else f"Добавить в {reference_table}")
        self.setModal(True)
        self.setup_interface()

    def setup_interface(self):
        """Создание интерфейса окна"""
        layout = QtWidgets.QVBoxLayout(self)

        # Форма с одним полем ввода (для справочников)
        form_layout = QtWidgets.QFormLayout()
        self.value_input = QtWidgets.QLineEdit()
        form_layout.addRow("Значение:", self.value_input)
        layout.addLayout(form_layout)

        # Если редактируем существующую запись
        if self.record_info:
            self.value_input.setText(self.record_info[1])

        # Кнопки действий
        buttons_layout = QtWidgets.QHBoxLayout()
        button_text = "Сохранить" if self.record_info else "Добавить"
        self.confirm_button = QtWidgets.QPushButton(button_text)
        self.confirm_button.clicked.connect(self.accept)
        self.abort_button = QtWidgets.QPushButton("Отмена")
        self.abort_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.confirm_button)
        buttons_layout.addWidget(self.abort_button)
        layout.addLayout(buttons_layout)

    def get_value(self):
        """Получение значения из поля ввода"""
        return self.value_input.text().strip()


class FindRecordsDialog(QtWidgets.QDialog):
    """Диалоговое окно для поиска записей"""

    def __init__(self, parent=None, table_name=""):
        super().__init__(parent)
        # Преобразуем техническое имя таблицы в отображаемое
        table_display_names = {
            "main": "Основная таблица",
            "fam": "Фамилии",
            "name": "Имена",
            "otc": "Отчества",
            "street": "Улицы"
        }
        display_name = table_display_names.get(table_name, table_name)
        self.setWindowTitle(f"Поиск: {display_name}")
        self.table_name = table_name
        self.setModal(True)
        self.setup_interface()

    def setup_interface(self):
        """Создание интерфейса окна"""
        layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout()
        self.search_inputs = {}

        # Разные поля поиска для основной и справочных таблиц
        if self.table_name == "main":
            # Поля для поиска в основной таблице
            fields = [
                ("Фамилия:", "surname", "Фамилия"),
                ("Имя:", "firstname", "Имя"),
                ("Отчество:", "patronymic", "Отчество"),
                ("Улица:", "street", "Улица"),
                ("Дом:", "house", "Дом"),
                ("Корпус:", "housing", "Корпус"),
                ("Квартира:", "apartment", "Квартира"),
                ("Телефон:", "phone", "Телефон")
            ]

            for label_text, field_name, placeholder in fields:
                self.search_inputs[field_name] = QtWidgets.QLineEdit()
                self.search_inputs[field_name].setPlaceholderText(placeholder)
                form_layout.addRow(label_text, self.search_inputs[field_name])
        else:
            # Одно поле для поиска в справочных таблицах
            self.search_inputs['value'] = QtWidgets.QLineEdit()
            self.search_inputs['value'].setPlaceholderText("Значение для поиска")
            form_layout.addRow("Значение:", self.search_inputs['value'])

        layout.addLayout(form_layout)

        # Кнопки действий
        buttons_layout = QtWidgets.QHBoxLayout()
        self.find_button = QtWidgets.QPushButton("Найти")
        self.find_button.clicked.connect(self.accept)
        self.cancel_button = QtWidgets.QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        self.reset_button = QtWidgets.QPushButton("Сброс")
        self.reset_button.clicked.connect(self.clear_inputs)

        buttons_layout.addWidget(self.find_button)
        buttons_layout.addWidget(self.reset_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

    def clear_inputs(self):
        """Очистка всех полей поиска"""
        for input_field in self.search_inputs.values():
            input_field.clear()

    def get_search_criteria(self):
        """Получение критериев поиска"""
        criteria = {}
        for field_name, input_widget in self.search_inputs.items():
            value = input_widget.text().strip()
            if value:
                criteria[field_name] = value
        return criteria


class MainApplicationWindow(QtWidgets.QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        # Настройка главного окна
        self.setWindowTitle("База данных адресов")
        self.setGeometry(500, 200, 1200, 600)

        # Создание центрального виджета
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Основной макет
        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        # ============================================
        # СОЗДАНИЕ ИНТЕРФЕЙСА
        # ============================================

        # 1. Выбор таблицы
        table_selection_layout = QtWidgets.QHBoxLayout()
        table_selection_layout.addWidget(QtWidgets.QLabel("Таблица:"))

        self.table_selector = QtWidgets.QComboBox()
        self.table_selector.addItems(["Основная таблица", "Фамилии", "Имена", "Отчества", "Улицы"])
        self.table_selector.currentTextChanged.connect(self.table_changed)
        table_selection_layout.addWidget(self.table_selector)

        # Растягивающийся элемент для выравнивания
        table_selection_layout.addStretch()
        main_layout.addLayout(table_selection_layout)

        # 2. Кнопки операций
        operations_layout = QtWidgets.QHBoxLayout()

        # Создаем кнопки с привязкой к функциям
        buttons_info = [
            ("Поиск", self.find_records),
            ("Добавить", self.add_record),
            ("Изменить", self.edit_record),
            ("Удалить", self.remove_record)
        ]

        for text, handler in buttons_info:
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(handler)
            operations_layout.addWidget(button)

        main_layout.addLayout(operations_layout)

        # 3. Таблица для отображения результатов с прокруткой
        table_container = QtWidgets.QWidget()
        table_container_layout = QtWidgets.QVBoxLayout(table_container)
        table_container_layout.setContentsMargins(0, 0, 0, 0)

        self.results_table = QtWidgets.QTableWidget()
        self.setup_table_appearance()
        table_container_layout.addWidget(self.results_table)

        # Добавляем контейнер с таблицей в основной макет
        main_layout.addWidget(QtWidgets.QLabel("Результаты:"))
        main_layout.addWidget(table_container)

        # 4. Строка состояния (внизу окна)
        self.status_display = self.statusBar()

        # Автоматически загружаем данные при запуске
        self.load_initial_data()

    def setup_table_appearance(self):
        """Настройка внешнего вида таблицы - растягивающиеся столбцы"""
        # Настройка выделения
        self.results_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.results_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Включаем автоматическое изменение размеров
        self.results_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        # Настройка отображения текста
        self.results_table.setWordWrap(True)
        self.results_table.setTextElideMode(QtCore.Qt.ElideNone)

        # Настройка заголовков столбцов - все столбцы растягиваются
        header = self.results_table.horizontalHeader()

        # Включаем растягивание последнего столбца
        header.setStretchLastSection(True)

        # Все столбцы будут растягиваться пропорционально
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Автоматическое изменение размера строк в зависимости от содержимого
        vertical_header = self.results_table.verticalHeader()
        vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # Альтернативный цвет строк
        self.results_table.setAlternatingRowColors(True)

        # Стиль таблицы (CSS)
        self.results_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f8f8f8;
                border: 1px solid #d0d0d0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 10px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
                font-size: 12px;
            }
            QTableCornerButton::section {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
            }
        """)

        # Настраиваем отображение текста в ячейках
        self.results_table.setFont(QtGui.QFont("Arial", 10))

        # Устанавливаем обработчик для автоматического расширения при редактировании
        self.results_table.itemChanged.connect(self.adjust_row_height)

    def adjust_row_height(self, item):
        """Автоматическая регулировка высоты строки при изменении содержимого"""
        # Пересчитываем высоту строки для измененной ячейки
        self.results_table.resizeRowToContents(item.row())

    def table_changed(self):
        """Обработчик изменения выбранной таблицы"""
        self.load_initial_data()

    def get_selected_table(self):
        """Получение технического имени выбранной таблицы"""
        display_to_technical = {
            "Основная таблица": "main",
            "Фамилии": "fam",
            "Имена": "name",
            "Отчества": "otc",
            "Улицы": "street"
        }
        display_name = self.table_selector.currentText()
        return display_to_technical[display_name]

    def load_initial_data(self):
        """Загрузка и отображение данных при запуске или смене таблицы"""
        current_table = self.get_selected_table()

        try:
            # Формируем SQL-запрос в зависимости от выбранной таблицы
            if current_table == "main":
                # Для основной таблицы делаем JOIN со справочниками
                query = """
                SELECT main.uniq_id, fam.f_val, name.n_val, otc.o_val, street.s_val, 
                       main.bldn, main.bldn_k, main.ap, main.teleph
                FROM main
                JOIN fam ON main.fam = fam.f_id
                JOIN name ON main.name = name.n_id
                JOIN otc ON main.otc = otc.o_id
                JOIN street ON main.street = street.s_id
                ORDER BY main.uniq_id
                """
                column_titles = ["ID", "Фамилия", "Имя", "Отчество", "Улица", "Дом", "Корпус", "Квартира", "Телефон"]
            else:
                # Для справочных таблиц
                table_queries = {
                    "fam": ("SELECT f_id, f_val FROM fam ORDER BY f_val", ["ID", "Фамилия"]),
                    "name": ("SELECT n_id, n_val FROM name ORDER BY n_val", ["ID", "Имя"]),
                    "otc": ("SELECT o_id, o_val FROM otc ORDER BY o_val", ["ID", "Отчество"]),
                    "street": ("SELECT s_id, s_val FROM street ORDER BY s_val", ["ID", "Улица"])
                }
                query, column_titles = table_queries[current_table]

            # Выполняем запрос к базе данных
            data = execute_sql_command(query)

            if data:
                # Настраиваем таблицу
                columns_count = len(data[0])
                self.results_table.setRowCount(len(data))
                self.results_table.setColumnCount(columns_count)
                self.results_table.setHorizontalHeaderLabels(column_titles)

                # Заполняем таблицу данными
                for row_index, row_data in enumerate(data):
                    for col_index, value in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(str(value) if value is not None else "")
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

                        # Устанавливаем выравнивание текста
                        item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

                        # Устанавливаем возможность переноса текста
                        item.setTextAlignment(QtCore.Qt.TextWordWrap)

                        self.results_table.setItem(row_index, col_index, item)

                # Автоматически подгоняем высоту строк по содержимому
                self.results_table.resizeRowsToContents()

                # Показываем количество записей в статусной строке
                self.status_display.showMessage(f"Загружено записей: {len(data)}")
            else:
                # Если данных нет
                self.results_table.clear()
                self.results_table.setRowCount(0)
                self.results_table.setColumnCount(0)
                self.status_display.showMessage("Нет данных для отображения")

        except Exception as error:
            # Обработка ошибок
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных:\n{str(error)}")
            self.status_display.showMessage("Ошибка загрузки данных")

    def find_records(self):
        """Поиск записей по значениям столбцов"""
        current_table = self.get_selected_table()
        search_dialog = FindRecordsDialog(self, current_table)

        if search_dialog.exec_() == QtWidgets.QDialog.Accepted:
            search_criteria = search_dialog.get_search_criteria()

            if not search_criteria:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите значения для поиска")
                return

            try:
                if current_table == "main":
                    query = self.build_main_search_query(search_criteria)
                else:
                    query = self.build_reference_search_query(current_table, search_criteria)

                if query:
                    self.execute_search_query(query, current_table)

            except Exception as error:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка поиска:\n{str(error)}")

    def build_main_search_query(self, search_criteria):
        """Построение SQL запроса для поиска в основной таблице"""
        base_query = """
        SELECT main.uniq_id, fam.f_val, name.n_val, otc.o_val, street.s_val, 
               main.bldn, main.bldn_k, main.ap, main.teleph
        FROM main
        JOIN fam ON main.fam = fam.f_id
        JOIN name ON main.name = name.n_id
        JOIN otc ON main.otc = otc.o_id
        JOIN street ON main.street = street.s_id
        """

        conditions = []
        field_mapping = {
            'surname': 'fam.f_val',
            'firstname': 'name.n_val',
            'patronymic': 'otc.o_val',
            'street': 'street.s_val',
            'house': 'main.bldn',
            'housing': 'main.bldn_k',
            'apartment': 'main.ap',
            'phone': 'main.teleph'
        }

        for field, value in search_criteria.items():
            if field in field_mapping:
                db_field = field_mapping[field]
                if field in ['house', 'housing', 'apartment']:
                    if value.isdigit():
                        conditions.append(f"{db_field} = {value}")
                    else:
                        QtWidgets.QMessageBox.warning(self, "Ошибка",
                                                      f"Поле '{field}' должно содержать только цифры")
                        return None
                else:
                    conditions.append(f"{db_field} ILIKE '%{value}%'")

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        return base_query + " ORDER BY main.uniq_id"

    def build_reference_search_query(self, table_name, search_criteria):
        """Построение SQL запроса для поиска в справочных таблицах"""
        if 'value' in search_criteria:
            value = search_criteria['value']
            return f"SELECT {table_name[0]}_id, {table_name[0]}_val FROM {table_name} WHERE {table_name[0]}_val ILIKE '%{value}%' ORDER BY {table_name[0]}_val"
        return f"SELECT {table_name[0]}_id, {table_name[0]}_val FROM {table_name} ORDER BY {table_name[0]}_val"

    def execute_search_query(self, query, table_name):
        """Выполнение поискового запроса и отображение результатов"""
        if query is None:
            return

        data = execute_sql_command(query)

        if data:
            # Определяем заголовки столбцов
            column_titles = {
                "main": ["ID", "Фамилия", "Имя", "Отчество", "Улица", "Дом", "Корпус", "Квартира", "Телефон"],
                "fam": ["ID", "Фамилия"],
                "name": ["ID", "Имя"],
                "otc": ["ID", "Отчество"],
                "street": ["ID", "Улица"]
            }

            titles = column_titles[table_name]
            columns_count = len(data[0])

            # Настраиваем таблицу
            self.results_table.setRowCount(len(data))
            self.results_table.setColumnCount(columns_count)
            self.results_table.setHorizontalHeaderLabels(titles)

            # Заполняем данными
            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value) if value is not None else "")
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

                    # Устанавливаем выравнивание текста
                    item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                    item.setTextAlignment(QtCore.Qt.TextWordWrap)

                    self.results_table.setItem(row_index, col_index, item)

            # Автоматически подгоняем высоту строк
            self.results_table.resizeRowsToContents()

            self.status_display.showMessage(f"Найдено записей: {len(data)}")
        else:
            self.results_table.clear()
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            self.status_display.showMessage("Поиск не дал результатов")

    def add_record(self):
        """Добавление новой записи"""
        current_table = self.get_selected_table()

        if current_table == "main":
            self.add_main_record()
        else:
            self.add_reference_record()

    def add_main_record(self):
        """Добавление записи в основную таблицу"""
        dialog = EditRecordDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            record_data = dialog.collect_data()

            # Проверка обязательных полей
            required_fields = ['surname', 'firstname', 'street', 'house', 'phone']
            for field in required_fields:
                if not record_data[field]:
                    QtWidgets.QMessageBox.warning(self, "Ошибка",
                                                  "Заполните обязательные поля: Фамилия, Имя, Улица, Дом, Телефон")
                    return

            try:
                # Проверяем и добавляем в справочники
                for field, table in [('surname', 'fam'), ('firstname', 'name'),
                                     ('patronymic', 'otc'), ('street', 'street')]:
                    value = record_data[field]
                    if value:
                        check_query = f"SELECT {table[0]}_id FROM {table} WHERE {table[0]}_val = '{value}'"
                        existing = execute_sql_command(check_query)
                        if not existing:
                            execute_sql_command(f"INSERT INTO {table} ({table[0]}_val) VALUES ('{value}')")

                # Обработка NULL значений
                housing_value = 'NULL' if not record_data['housing'] else record_data['housing']
                apartment_value = 'NULL' if not record_data['apartment'] else record_data['apartment']

                # Формируем запрос на добавление
                query = f"""
                INSERT INTO main (fam, name, otc, street, bldn, bldn_k, ap, teleph)
                VALUES (
                    (SELECT f_id FROM fam WHERE f_val = '{record_data['surname']}'),
                    (SELECT n_id FROM name WHERE n_val = '{record_data['firstname']}'),
                    (SELECT o_id FROM otc WHERE o_val = '{record_data['patronymic']}'),
                    (SELECT s_id FROM street WHERE s_val = '{record_data['street']}'),
                    {record_data['house']},
                    {housing_value},
                    {apartment_value},
                    '{record_data['phone']}'
                )
                """

                execute_sql_command(query)
                self.load_initial_data()
                QtWidgets.QMessageBox.information(self, "Успех", "Запись добавлена")

            except Exception as error:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка добавления:\n{str(error)}")

    def add_reference_record(self):
        """Добавление записи в справочную таблицу"""
        current_table = self.get_selected_table()
        dialog = EditReferenceDialog(self, reference_table=current_table)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            value = dialog.get_value()

            if not value:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите значение")
                return

            try:
                # Проверка на дубликат
                check_query = f"SELECT * FROM {current_table} WHERE {current_table[0]}_val = '{value}'"
                existing = execute_sql_command(check_query)

                if existing:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Такое значение уже существует")
                    return

                # Добавление записи
                query = f"INSERT INTO {current_table} ({current_table[0]}_val) VALUES ('{value}')"
                execute_sql_command(query)
                self.load_initial_data()
                QtWidgets.QMessageBox.information(self, "Успех", "Запись добавлена")

            except Exception as error:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка добавления:\n{str(error)}")

    def edit_record(self):
        """Редактирование записи"""
        current_table = self.get_selected_table()

        if current_table == "main":
            self.edit_main_record()
        else:
            self.edit_reference_record()

    def edit_main_record(self):
        """Редактирование записи в основной таблице"""
        current_row = self.results_table.currentRow()
        if current_row >= 0:
            # Получаем ID выбранной записи
            record_id = self.results_table.item(current_row, 0).text()

            # Собираем данные выбранной записи
            record_info = []
            for column in range(self.results_table.columnCount()):
                record_info.append(self.results_table.item(current_row, column).text())

            # Открываем диалог редактирования
            dialog = EditRecordDialog(self, record_info)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                record_data = dialog.collect_data()

                try:
                    # Обновляем справочники при необходимости
                    for field, table in [('surname', 'fam'), ('firstname', 'name'),
                                         ('patronymic', 'otc'), ('street', 'street')]:
                        value = record_data[field]
                        if value:
                            check_query = f"SELECT {table[0]}_id FROM {table} WHERE {table[0]}_val = '{value}'"
                            existing = execute_sql_command(check_query)
                            if not existing:
                                execute_sql_command(f"INSERT INTO {table} ({table[0]}_val) VALUES ('{value}')")

                    # Обработка NULL значений
                    housing_value = 'NULL' if not record_data['housing'] or record_data['housing'] == 'None' else \
                    record_data['housing']
                    apartment_value = 'NULL' if not record_data['apartment'] or record_data['apartment'] == 'None' else \
                    record_data['apartment']

                    # Формируем запрос на обновление
                    query = f"""
                    UPDATE main SET
                        fam = (SELECT f_id FROM fam WHERE f_val = '{record_data['surname']}'),
                        name = (SELECT n_id FROM name WHERE n_val = '{record_data['firstname']}'),
                        otc = (SELECT o_id FROM otc WHERE o_val = '{record_data['patronymic']}'),
                        street = (SELECT s_id FROM street WHERE s_val = '{record_data['street']}'),
                        bldn = {record_data['house']},
                        bldn_k = {housing_value},
                        ap = {apartment_value},
                        teleph = '{record_data['phone']}'
                    WHERE uniq_id = {record_id}
                    """

                    execute_sql_command(query)
                    self.load_initial_data()
                    QtWidgets.QMessageBox.information(self, "Успех", "Запись изменена")

                except Exception as error:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка изменения:\n{str(error)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для изменения")

    def edit_reference_record(self):
        """Редактирование записи в справочной таблице"""
        current_row = self.results_table.currentRow()
        if current_row >= 0:
            record_id = self.results_table.item(current_row, 0).text()
            record_value = self.results_table.item(current_row, 1).text()
            current_table = self.get_selected_table()

            dialog = EditReferenceDialog(self, (record_id, record_value), current_table)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                new_value = dialog.get_value()

                if not new_value:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите значение")
                    return

                try:
                    # Проверка на дубликат
                    check_query = f"SELECT * FROM {current_table} WHERE {current_table[0]}_val = '{new_value}' AND {current_table[0]}_id != {record_id}"
                    existing = execute_sql_command(check_query)

                    if existing:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", "Такое значение уже существует")
                        return

                    # Обновление записи
                    query = f"UPDATE {current_table} SET {current_table[0]}_val = '{new_value}' WHERE {current_table[0]}_id = {record_id}"
                    execute_sql_command(query)
                    self.load_initial_data()
                    QtWidgets.QMessageBox.information(self, "Успех", "Запись изменена")

                except Exception as error:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка изменения:\n{str(error)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для изменения")

    def remove_record(self):
        """Удаление записи"""
        current_table = self.get_selected_table()

        if current_table == "main":
            self.remove_main_record()
        else:
            self.remove_reference_record()

    def remove_main_record(self):
        """Удаление записи из основной таблицы"""
        current_row = self.results_table.currentRow()
        if current_row >= 0:
            record_id = self.results_table.item(current_row, 0).text()

            # Подтверждение удаления
            reply = QtWidgets.QMessageBox.question(
                self, "Подтверждение",
                f"Вы уверены, что хотите удалить запись ID: {record_id}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    # Удаление записи
                    query = f"DELETE FROM main WHERE uniq_id = {record_id}"
                    execute_sql_command(query)

                    self.load_initial_data()
                    QtWidgets.QMessageBox.information(self, "Успех", "Запись удалена")

                except Exception as error:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка удаления:\n{str(error)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")

    def remove_reference_record(self):
        """Удаление записи из справочной таблицы (с проверкой использования)"""
        current_row = self.results_table.currentRow()
        if current_row >= 0:
            record_id = self.results_table.item(current_row, 0).text()
            record_value = self.results_table.item(current_row, 1).text()
            current_table = self.get_selected_table()

            # ПРОВЕРКА: используется ли запись в основной таблице
            try:
                # Для каждой таблицы свой столбец в основной таблице
                column_map = {
                    'fam': 'fam',
                    'name': 'name',
                    'otc': 'otc',
                    'street': 'street'
                }

                main_column = column_map.get(current_table)
                if main_column:
                    # Проверяем, сколько записей в основной таблице используют эту запись
                    check_query = f"""
                    SELECT COUNT(*) as usage_count, 
                           STRING_AGG(main.uniq_id::text, ', ') as ids
                    FROM main 
                    WHERE {main_column} = {record_id}
                    """

                    result = execute_sql_command(check_query)

                    if result and result[0][0] > 0:
                        usage_count = result[0][0]
                        record_ids = result[0][1]

                        # Показываем сообщение об ошибке с информацией
                        QtWidgets.QMessageBox.warning(
                            self, "Ошибка удаления",
                            f"Невозможно удалить запись '{record_value}'.\n\n"
                            f"Она используется в {usage_count} записях основной таблицы.\n"
                            f"ID записей: {record_ids}\n\n"
                            f"Сначала удалите эти записи из основной таблицы."
                        )
                        return

                # Если запись не используется - запрашиваем подтверждение
                reply = QtWidgets.QMessageBox.question(
                    self, "Подтверждение",
                    f"Вы уверены, что хотите удалить запись: '{record_value}'?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )

                if reply == QtWidgets.QMessageBox.Yes:
                    # Удаляем запись
                    query = f"DELETE FROM {current_table} WHERE {current_table[0]}_id = {record_id}"
                    execute_sql_command(query)

                    self.load_initial_data()
                    QtWidgets.QMessageBox.information(self, "Успех", "Запись удалена")

            except Exception as error:
                # Обработка ошибок базы данных
                error_msg = str(error)
                if "foreign key constraint" in error_msg.lower():
                    QtWidgets.QMessageBox.critical(
                        self, "Ошибка",
                        f"Невозможно удалить запись '{record_value}'.\n\n"
                        f"Она используется в основной таблице.\n"
                        f"Сначала удалите связанные записи из основной таблицы."
                    )
                else:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка удаления:\n{error_msg}")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")


# ЗАПУСК ПРИЛОЖЕНИЯ

if __name__ == "__main__":
    # Настройка масштабирования для высоких DPI
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # Создаем объект приложения
    application = QtWidgets.QApplication(sys.argv)

    # Создаем и показываем главное окно
    main_window = MainApplicationWindow()
    main_window.show()

    # Запускаем главный цикл приложения
    sys.exit(application.exec_())