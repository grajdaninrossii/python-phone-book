from tabulate import tabulate # бибилиотека/ для красоты вывода
from database import PhoneBookDatabase


class PhoneBookService:
    '''
    Класс, содержащий бизнес-логику приложения.
    '''

    __header_table: list[str] = ["uuid","фамилия", "имя","отчество", "название_организации","телефон_рабочий", "телефон_личный_(сотовый)"] # названия столбцов таблицы
    __file_not_found_error_text = "Телефонная книга еще не создана! Добавьте данные в книгу, она создастся автоматически."

    def __init__(self, phonebookDatabase: PhoneBookDatabase):
        self.database = phonebookDatabase


    async def __is_validated_record(self, record: str) -> (str, bool):
        '''
        Проверка валидности строки. Также можно сюда в дальнейшем добавить регулярку на поля.
        '''
        data_record: list[str] = [x.strip() for x in record.split()]
        is_validated_record: bool = len(data_record) == 6 and all([len(x) != 0 for x in data_record]) # проверяем корректность ввода на кол-во записей и длину самих записей
        validated_record: str = ", ".join(data_record) # переводим в строку
        is_added: bool | None = await self.database.is_added_record(validated_record)
        if is_added is None:
            raise FileNotFoundError(self.__file_not_found_error_text)
        is_validated_record = is_validated_record and not is_added # проверяем наличие записи в бд
        return validated_record, is_validated_record


    async def print_all_records(self) -> None:
        '''Вывод всех записей на экран

        '''
        data: list[list[str]] | None = await self.database.get_all_records()
        # print(data)
        if data != []:
            print(tabulate(data, headers=[x.replace("_", "\n") for x in self.__header_table])) # красиво выводим таблицу
        elif data is None:
            print(self.__file_not_found_error_text)
        else:
            print("Телефонная книга пуста! Добавьте данные!")


    async def add_record(self, record: str) -> None:
        '''Добавление новой записи в справочник

        '''
        try:
            validated_record, is_valid_data = await self.__is_validated_record(record)
        except FileNotFoundError as e:
            await self.database.create_phone_book()
            validated_record, is_valid_data = await self.__is_validated_record(record)
            # print(str(e))

        # Проверка валидности строки.
        if is_valid_data:
            await self.database.add_record(validated_record + "\n")
            print('Данные сохранены!') # successful addition
        else:
            print("Ошибка! Данные несохраненны! Проверьте валидность записи и/или ее наличие в базе книги!")


    async def edit_record(self, record_uuid, edited_record) -> None:
        '''Редактирование записи в справочнике

        '''
        try:
            validated_record, is_valid_data = await self.__is_validated_record(edited_record)
        except FileNotFoundError as e:
            print(str(e))
            return None

        if is_valid_data:
            result = await self.database.edit_record(record_uuid, validated_record + "\n")
            if result is not None:
                print(result)
            else:
                print("Ошибка!")


    async def print_found_records(self, characteristics: dict[str, str]) -> None:
        '''Поиск записей по одной или нескольким характеристикам

        '''
        data: list[list[str]] | None = await self.database.get_all_records()
        if data is None:
            print(self.__file_not_found_error_text)
            return None
        characteristics_items: list = list(characteristics.items())
        for key, value in characteristics_items:
            el_id = self.__header_table.index(key) # берем номер критерия поиска
            data = list(filter(lambda x: x[el_id] == value, data))
        if data != []:
            print(f"Поиск по условию/ям: {characteristics_items}")
            print(tabulate(data, headers=[x.replace("_", "\n") for x in self.__header_table]))
        else:
            print("Нет записий по данному критерию.")