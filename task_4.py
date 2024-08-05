import logging
import oopTask

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    
    name, phone = args
    if name in book.data:
        raise ValueError("Contact already exists. Use 'change' command to update the contact.")
    
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    
    logging.info(f"Contact added: {name} - {phone}")
    return "Contact added."

def change_contact(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(phone, phone)
        logging.info(f"Contact updated: {name} - {phone}")
        return "Contact updated."
    else:
        raise KeyError("Contact not found.")

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

def show_all(book):
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts found."

def main():
    book = AddressBook()
    logging.info("Bot started.")
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
            else:
                logging.warning(f"Invalid command entered: {command}")
                print("Invalid command.")
        except Exception as e:
            logging.error(str(e))
            print(str(e))

if __name__ == "__main__":
    main()