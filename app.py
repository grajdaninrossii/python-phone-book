import asyncio

from database import PhoneBookDatabase
from services import PhoneBookService

# Основная функция работы с пользователем
async def main():
    data: str = "\nЯ телефонный справчник. Для тебя я могу:\n" +\
                "1. Постранично вывести все записи;\n" +\
                "2. Добавить новую запись;\n" +\
                "3. Редактировать запись;\n" +\
                "4. Найти записи по заданной характеристике.\n" +\
                "Чтобы выйти из программы введите: 0"


    # Настройка зависимостей
    database: PhoneBookDatabase = PhoneBookDatabase()
    phone_book_service: PhoneBookService = PhoneBookService(database)
    action: int = 1

    # Программа работает до тех пор, пока пользователь не введет 0 в главном меню
    while action != 0:
        # Инициализация начального действия
        # Вывод начальной информации
        print(data)
        try:
            action = int(input("Введите выбранное действие(1-4): "))
        except ValueError:
            print("Ошибка ввода! Введите цифру от 1 до 4 (включительно)!")
            continue

        # Выбор функции для выполнения.
        # Если бы действий было слишком много, то можно было бы сохранить функции в dict (ключ: function), так было бы проще их после вызывать.
        match action:
            case 1:
                await phone_book_service.print_all_records()
            case 2:
                new_record: str = input("Обязательны поля: [фамилия] [имя] [отчество] [название организации] [телефон рабочий] [телефон личный (сотовый)]\nВведите новую запись:")
                await phone_book_service.add_record(new_record)
            case 3:
                record_id: str = input("Введите uuid записи: ")
                edited_record: str = input("Введите измененную запись ([фамилия] [имя] [отчество] [название организации] [телефон рабочий] [телефон личный (сотовый)]): ")
                await phone_book_service.edit_record(record_id, edited_record)
            case 4:
                hint: str = "\nДля ввода характеристик из нескольких слов используйте _ (телефон_рабочий)\nВведите характеристики и значения фильтрации через запятую (имя:[имя] фамилия:[фамилия]): "
                try:
                    characteristics: dict[str, str] = dict([x.split(":") for x in input(hint).split()]) # парсим характиристики и значения, после сохраняем в словарь
                except ValueError:
                    print("Вводите данные согласно образцу!! (имя:[имя] фамилия:[фамилия])")
                await phone_book_service.print_found_records(characteristics)


# Запуск приложения
if __name__ == "__main__":
    asyncio.run(main())