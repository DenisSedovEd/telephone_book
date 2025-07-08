import os
import tempfile
import pytest
from model import PhoneBook, Contact
from my_exception import (
    FileNotOpenedError,
    TryOpenFileError,
    IncorrectPhoneNumberDigit,
    InvalidPhoneNumberLatter,
)


@pytest.fixture
def temp_phonebook(tmp_path):
    test_file = tmp_path / "test_phonebook.txt"

    if not test_file.exists():
        test_file.write_text(
            "John Doe;1234567890;Friend\n" "Jane Smith;0987654321;Work\n",
            encoding="utf-8",
        )

    phonebook = PhoneBook(path=str(test_file))
    phonebook.open_file()
    return phonebook


def test_open_file_success(temp_phonebook):
    """Тестирование успешного открытия файла"""
    assert len(temp_phonebook.phone_book) == 2
    assert "John Doe" in [
        contact.name for contact in temp_phonebook.phone_book.values()
    ]
    assert "Jane Smith" in [
        contact.name for contact in temp_phonebook.phone_book.values()
    ]


def test_open_file_already_opened(temp_phonebook):
    """Тестирование попытки открыть уже открытый файл"""
    with pytest.raises(TryOpenFileError):
        temp_phonebook.open_file()


def test_add_contact_success(temp_phonebook):
    """Тестирование успешного добавления контакта"""
    initial_count = len(temp_phonebook.phone_book)
    new_contact = ["Alice Wonderland", "5551234567", "Friend"]
    assert temp_phonebook.new_contact(new_contact) is True
    assert len(temp_phonebook.phone_book) == initial_count + 1
    assert "Alice Wonderland" in [
        contact.name for contact in temp_phonebook.phone_book.values()
    ]


@pytest.mark.parametrize(
    "phone_number, expected_exception",
    [
        ("123456789012", IncorrectPhoneNumberDigit),  # Слишком длинный номер
        ("12a3456789", InvalidPhoneNumberLatter),  # Буквы в номере
        ("", InvalidPhoneNumberLatter),  # Пустой номер
    ],
)
def test_add_contact_invalid_phone(temp_phonebook, phone_number, expected_exception):
    """Тестирование добавления контакта с невалидным номером"""
    with pytest.raises(expected_exception):
        temp_phonebook.new_contact(["Bob", phone_number, "Colleague"])


def test_edit_contact_success(temp_phonebook):
    """Тестирование успешного редактирования контакта"""
    contact_id = next(iter(temp_phonebook.phone_book))
    edited_contact = ["John Updated", "1112223344", "Updated"]
    temp_phonebook.edit_contact(str(contact_id), edited_contact)

    contact = temp_phonebook.phone_book[contact_id]
    assert contact.name == "John Updated"
    assert contact.phone == "1112223344"
    assert contact.comment == "Updated"


def test_edit_nonexistent_contact(temp_phonebook):
    """Тестирование редактирования несуществующего контакта"""
    with pytest.raises(KeyError):
        temp_phonebook.edit_contact("999", ["Nonexistent", "123", "Test"])


def test_find_contact(temp_phonebook):
    """Тестирование поиска контакта"""
    # Поиск по имени
    results = temp_phonebook.find_contact("John")
    assert len(results) == 1
    assert "John Doe" in [contact.name for contact in results.values()]

    # Поиск по номеру
    results = temp_phonebook.find_contact("1234567890")
    assert len(results) == 1
    assert "1234567890" in [contact.phone for contact in results.values()]

    # Поиск по комментарию
    results = temp_phonebook.find_contact("Work")
    assert len(results) == 1
    assert "Jane Smith" in [contact.name for contact in results.values()]

    # Поиск несуществующего контакта
    results = temp_phonebook.find_contact("Nonexistent")
    assert len(results) == 0


def test_delete_contact_success(temp_phonebook):
    """Тестирование успешного удаления контакта"""
    initial_count = len(temp_phonebook.phone_book)
    contact_id = next(iter(temp_phonebook.phone_book))

    deleted_contact = temp_phonebook.delete_contact(str(contact_id))
    assert deleted_contact is not None
    assert len(temp_phonebook.phone_book) == initial_count - 1
    assert contact_id not in temp_phonebook.phone_book


def test_delete_nonexistent_contact(temp_phonebook):
    """Тестирование удаления несуществующего контакта"""
    with pytest.raises(KeyError):
        temp_phonebook.delete_contact("999")


def test_save_file(temp_phonebook, tmp_path):
    """Тестирование сохранения файла"""
    # Создаем временный файл для сохранения
    temp_save_path = tmp_path / "saved_phonebook.txt"
    temp_phonebook.path = str(temp_save_path)

    # Сохраняем и проверяем, что файл создан
    temp_phonebook.save_file()
    assert os.path.exists(temp_save_path)

    # Проверяем содержимое файла
    with open(temp_save_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "John Doe" in content
        assert "Jane Smith" in content


def test_operations_without_opening_file():
    """Тестирование операций без предварительного открытия файла"""
    phonebook = PhoneBook("nonexistent.txt")

    with pytest.raises(FileNotOpenedError):
        phonebook.new_contact(["Test", "123", "Test"])

    with pytest.raises(FileNotOpenedError):
        phonebook.edit_contact("1", ["Test", "123", "Test"])

    with pytest.raises(FileNotOpenedError):
        phonebook.delete_contact("1")

    with pytest.raises(FileNotOpenedError):
        phonebook.save_file()


# Дополнительные тесты на граничные случаи
def test_add_empty_contact(temp_phonebook):
    """Тестирование добавления контакта с пустыми полями"""
    # Проверяем, что можно добавить контакт с пустыми полями, кроме телефона
    with pytest.raises(InvalidPhoneNumberLatter):
        temp_phonebook.new_contact(["", "", ""])  # Пустой номер телефона

    # Проверяем добавление с пустыми именем и комментарием, но валидным номером
    temp_phonebook.new_contact(["", "1234567890", ""])
    assert "" in [contact.name for contact in temp_phonebook.phone_book.values()]


def test_find_with_empty_query(temp_phonebook):
    """Тестирование поиска с пустым запросом"""
    # Поиск с пустым запросом должен вернуть все контакты
    results = temp_phonebook.find_contact("")
    assert len(results) == len(temp_phonebook.phone_book)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
