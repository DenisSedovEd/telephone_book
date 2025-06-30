from dataclasses import dataclass
from my_exception import *

@dataclass
class Contact:
    name: str
    phone: str
    comment: str

    def join(self, separator: str = ' '):
        '''
        Объединяем все параметры экземпляра класса Contact.
        :param separator:
        :return:
        '''
        data = [self.name, self.phone, self.comment]
        return separator.join(data)

    def compare(self, other: 'Contact'):
        '''
        Функция сравнения 2-х объектов класса Contact.
        :param other:
        :return:
        '''
        self.name = other.name if other.name else self.name
        self.phone = other.phone if other.phone else self.phone
        self.comment = other.comment if other.comment else self.comment


class PhoneBook:
    def __init__(self, path: str = 'phone_book.txt', separator: str = ';'):
        self.path = path
        self.separator = separator
        self.phone_book: dict[int, Contact] = {}

    def _next_id(self):
        '''
        Генерация ID.
        :return:
        '''
        if self.phone_book:
            return max(self.phone_book) + 1
        return 1

    def open_file(self):
        '''
        Открытие файла .txt (телефонного справочника)
        :return:
        '''
        with open(self.path, 'r', encoding='UTF-8') as file:
            data = list(map(lambda x: x.strip().split(self.separator), file.readlines()))
        if not self.phone_book:
            for entry in data:
                self.phone_book[self._next_id()] = Contact(
                    name=entry[0],
                    phone=entry[1],
                    comment=entry[2],
                )
            return True
        else:
            raise TryOpenFileError

    def save_file(self):
        '''
        Сохраняем файл.
        :return:
        '''
        with open(self.path, 'w', encoding='UTF-8') as file:
            data = [entry.join(self.separator) for entry in self.phone_book.values()]
            file.write('\n'.join(data))

    def new_contact(self, new_contact: list[str]):
        '''
        Функция добавления нового контакта
        :param new_contact:
        :return:
        '''
        current_id = self._next_id()
        if len(new_contact[1]) > 11 :
            raise IncorrectPhoneNumberDigit()
        elif not new_contact[1].isdigit():
            raise InvalidPhoneNumberLatter()
        if not self.phone_book:
            raise FileNotOpenedError
        else:
            self.phone_book[current_id] = Contact(
                name=new_contact[0],
                phone=new_contact[1],
                comment=new_contact[2],
            )
            return True

    def edit_contact(self, edit_id: str, edited_contact: list[str]):
        '''
        Изменения, выбранного по ID, контакта
        :param edit_id:
        :param edited_contact:
        :return:
        '''
        if not self.phone_book:
            raise FileNotOpenedError
        contact = self.phone_book[int(edit_id)]
        edited_contact = Contact(
            name=edited_contact[0],
            phone=edited_contact[1],
            comment=edited_contact[2],
        )
        if len(edited_contact.phone) > 11 :
            raise IncorrectPhoneNumberDigit()
        elif not edited_contact.phone.isdigit():
            raise InvalidPhoneNumberLatter()
        contact.compare(edited_contact)
        self.phone_book[int(edit_id)] = contact

    def find_contact(self, key_word: str) -> dict[int, Contact]:
        '''
        Функция поиска контакта по ключевому слову.
        :param key_word:
        :return:
        '''
        result = {}
        for idx, contact in self.phone_book.items():
            if key_word.lower() in contact.join().lower():
                result[idx] = contact
        return result

    def delete_contact(self, delete_id: str):
        '''
        Удаляем контакт.
        :param delete_id:
        :return:
        '''
        if self.phone_book:
            contact = self.phone_book.pop(int(delete_id))
        else:
            raise FileNotOpenedError
        return contact
