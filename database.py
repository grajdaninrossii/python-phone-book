import aiofiles
import uuid


class PhoneBookDatabase:


    # __pagination_count_row: int = 1000 # можно настроить для вывода и оптимизации вывода

    def __init__(self):
        pass


    async def get_all_records(self) -> list[str] | None:
        ''' Получение всех записей из файла
        '''
        try:
            async with aiofiles.open("./phone_book.txt", "r") as fl:
                records: list[str] = [line.rstrip().split(", ") for line in await fl.readlines()]
        except FileNotFoundError:
            return None
        return records


    async def add_record(self, new_record: str) -> None:
        ''' Сохранение в файл(телефонный справочник) записи

        '''
        async with aiofiles.open("./phone_book.txt", "a+") as fl:
            await fl.write(f'{str(uuid.uuid4())}, {new_record}')


    async def create_phone_book(self) -> None:
        ''' Создание файла phone_book.txt

        '''
        async with aiofiles.open("./phone_book.txt", "a+") as fl:
            await fl.write('')


    async def is_added_record(self, record: str) -> bool:
        ''' Проверка на существование исходной записи в базе данных(файле)

        '''
        try:
            async with aiofiles.open("./phone_book.txt", "r") as fl:
                line: str = await fl.readline() # читаем файл по-строчно
                while line:
                    line = line.rstrip('\n')
                    line = ", ".join(line.split(", ")[1:])
                    if record == line:
                        return True
                    line = await fl.readline()
        except FileNotFoundError:
            return None
        return False


    async def edit_record(self, record_uuid: str, edited_record: str) -> str | None:
        ''' Редактирование записи

        '''
        # Находим запись для редактирования
        async with aiofiles.open("./phone_book.txt", "r") as fl:
            lines: list[str] = await fl.readlines()
            for i in range(len(lines)):
                # Находим запись по uuid, после меняем ее в списке и выходим из цикла
                if lines[i].split(", ")[0] == record_uuid:
                    lines[i] = f'{record_uuid}, {edited_record}'
                    break
        # После записываем все данные из файла заново
        async with aiofiles.open("./phone_book.txt", "w") as fl:
            await fl.writelines(lines)
        return "Запись редактирована!"


    # async def get_thousand_record(self) -> list[str]:
    #     ''' Получение "безопасного" для чтения числа записей из файла

    #     '''

    #     async with open("./phone_book.txt", "r") as fl:
    #         records: list[str] = [await fl.readline() for _ in range(self.__pagination_count_row)]

    #     return records

# Создание объекта класса базы данных
phonebookDatabase: PhoneBookDatabase = PhoneBookDatabase()