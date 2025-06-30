import text
import view
from model import PhoneBook
from my_exception import *

PATH = "phone_book.txt"


def menu_item_1(pb: PhoneBook):
    """
    Функция меню
    :param pb:
    :return:
    """
    pb.open_file()
    view.print_message(text.phone_book_open_successful)


def menu_item_2(pb: PhoneBook):
    try:
        pb.save_file()
        view.print_message(text.phone_book_save_successful)
    except:
        raise MenuCommandError


def menu_item_3(pb: PhoneBook):
    phonebook = pb.phone_book
    view.show_contacts(phonebook, text.empty_phone_book_error)


def menu_item_4(pb: PhoneBook):
    try:
        new_contact = view.input_data(text.input_new_contact)
        pb.new_contact(new_contact)
    except IncorrectPhoneNumberDigit:
        view.print_message(text.incorrect_phone_number_digit)
    except InvalidPhoneNumberLatter:
        view.print_message(text.incorrect_phone_number_latter)
    except FileNotOpenedError:
        view.print_message(text.empty_phone_book_error)


def menu_item_5(pb: PhoneBook):
    edit_id = view.input_data(text.input_id_contact_to_edit)
    edited_contact = view.input_data(text.input_edited_contact)
    try:
        pb.edit_contact(edit_id, edited_contact)
    except IncorrectPhoneNumberDigit:
        view.print_message(text.incorrect_phone_number_digit)
    except InvalidPhoneNumberLatter:
        view.print_message(text.incorrect_phone_number_latter)
    except FileNotOpenedError:
        view.print_message(text.empty_phone_book_error)


def menu_item_6(pb: PhoneBook):
    key_word = view.input_data(text.input_key_word)
    result = pb.find_contact(key_word)
    view.show_contacts(result, text.no_result_error)


def menu_item_7(pb: PhoneBook):
    delete_id = view.input_data(text.input_delete_id)
    contact = pb.delete_contact(delete_id)
    view.print_message(text.delete_contact_successful.format(contact.name))


def menu_item_8(pb: PhoneBook):
    exit()


def start_app():
    pb = PhoneBook(PATH)
    while True:
        view.show_menu()
        user_choice = view.input_menu_item()
        menu_items = {
            1: menu_item_1,
            2: menu_item_2,
            3: menu_item_3,
            4: menu_item_4,
            5: menu_item_5,
            6: menu_item_6,
            7: menu_item_7,
            8: menu_item_8,
        }
        menu_items[user_choice](pb)
