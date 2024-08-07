import logging
import privatbankAPI
import pickle
from oopTask import AddressBook, Record, Name, Phone, Field, Birthday
from datetime import datetime

def show_help():
    help_text = (
        "Available commands:\n"
        "- hello: Greets the user.\n"
        "- add [contact details]: Adds a new contact.\n"
        "- change [contact details]: Changes an existing contact.\n"
        "- phone [contact name]: Shows the phone number of the contact.\n"
        "- all: Shows all contacts.\n"
        "- add-birthday [contact details]: Adds a birthday to a contact.\n"
        "- show-birthday [contact name]: Shows the birthday of the contact.\n"
        "- birthdays: Shows all upcoming birthdays.\n"
        "- exchange: Shows the current exchange rates from PrivatBank.\n"
        "- close / exit: Saves data and exits the application.\n"
        "- help: Shows this help message."
    )
    return help_text

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


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

def confirm_save():
    while True:
        confirm = input("Do you really want to save the data before exiting? (yes/no): ").strip().lower()
        if confirm == "yes":
            return True
        elif confirm == "no":
            return False
        else:
            print("Invalid command.")




def main():
    book = load_data()
    # book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        try:
            if command in ["close", "exit"]:
                if confirm_save():
                    save_data(book)
                    print("Result has been saved. Goodbye!")
                else:
                    print("Changes were not saved. Goodbye!")
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
            elif command == "exchange":
                print(privatbankAPI.get_exchange_rates())
            elif command == "help":
                print(show_help())
            else:
                print("Invalid command.")
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    main()
    # test()
