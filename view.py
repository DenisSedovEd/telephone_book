import text
from model import Contact, PhoneBook


def show_menu():
    '''
    Функция вывода главного меню.
    :return:
    '''
    for idx, row in enumerate(text.menu_items):
        if idx:
            print(f'\t{idx}. {row}')
        else:
            print(f'\n{row}')


def input_menu_item():
    '''
    Принимаем от пользователя выбранный пункт меню.
    :return:
    '''
    while True:
        user_choice = input(f'\n{text.input_menu_item}')
        if user_choice.isdigit() and 0 < int(user_choice) < len(text.menu_items):
            return int(user_choice)
        print(text.input_menu_error)


def show_contacts(phonebook: dict[int, Contact], msg_error: str):
    '''
    Вывод всех контактов телефонного справочника.
    :param phonebook:
    :param msg_error:
    :return:
    '''
    if phonebook:
        for idx, contact in phonebook.items():
            print(f'{idx}. {contact.name: <20} {contact.phone:<20} {contact.comment:<20}')
    else:
        print_message(msg_error)


def input_data(msg_to_input: list[str] | str) -> list[str] | str:
    '''
    Функция для ввода данных пользователем
    :param msg_to_input:
    :return:
    '''
    if isinstance(msg_to_input, list):
        result = []
        for msg in msg_to_input:
            entry = input(msg)
            result.append(entry)
        return result
    result = input(msg_to_input)
    return result

def print_message(msg: str):
    '''
    Функция печати сообщения для пользователя
    :param msg:
    :return:
    '''
    print('-'*(len(msg)+1))
    print(msg)
    print('-'*(len(msg)+1))
