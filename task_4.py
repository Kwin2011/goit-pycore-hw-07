import logging
from oopTask import AddressBook, Record, Name, Phone, Field, Birthday
from datetime import datetime

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Give me the name please.")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    elif record:
        return "No birthday set for this contact."
    else:
        raise KeyError("Contact not found.")

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(str(record) for record in upcoming_birthdays)
    else:
        return "No upcoming birthdays in the next 7 days."


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    # print(args)
    return cmd, args

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    
    name, phone = args[0], args[1]
    if name in book.data:
        raise ValueError("Contact already exists. Use 'change' command to update the contact.")
    
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    
    logging.info(f"Contact added: {name} - {phone}")
    return "Contact added."

@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")
    
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        logging.info(f"Contact updated: {name} - {new_phone}")
        return "Contact updated."
    else:
        raise KeyError("Contact not found.")

@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Enter the argument for the command.")
    
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        logging.info(f"Phone number retrieved for: {name}")
        return phones
    else:
        raise KeyError("Contact not found.")

@input_error
def show_all(book):
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts found."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        try:
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))
            else:
                print("Invalid command.")
        except Exception as e:
            print(str(e))

def test():
    book = AddressBook()

    # Додавання контактів з правильними номерами телефонів
    try:
        print(add_contact(parse_input("add Stefan 9999999999")[1], book))
    except ValueError as e:
        print(e)

    try:
        print(add_contact(parse_input("add Anna 1234567890")[1], book))
    except ValueError as e:
        print(e)

    # Показ телефонних номерів
    print(show_phone(["Stefan"], book))
    print(show_phone(["Anna"], book))

    # Додавання днів народження
    try:
        print(add_birthday(parse_input("add-birthday Stefan 06.01.1997")[1], book))
    except ValueError as e:
        print(e)

    try:
        print(add_birthday(parse_input("add-birthday Anna 22.07.1995")[1], book))
    except ValueError as e:
        print(e)


    print(show_birthday(["Stefan"], book))
    print(show_birthday(["Anna"], book))

    print(show_all(book))
    print("_______________")


    # Зміна телефонного номера
    try:
        print(change_contact(parse_input("change Stefan 9999999999 0987654321")[1], book))
    except ValueError as e:
        print(e)

    print(show_phone(["Stefan"], book))


    print(show_all(book))

    # Показ днів народження, які відбудуться протягом наступного тижня
    print(birthdays([], book))


if __name__ == "__main__":
    main()
    # test()
