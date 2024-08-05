from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Клас для зберігання номера телефону. Має валідацію формату (10 цифр)")
        super().__init__(value)

    @staticmethod
    def validate(phone):
        return phone.isdigit() and len(phone) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

class AddressBook(UserDict):
#     Функціональність:
#     AddressBook:Додавання записів.
    def add_record(self, record):
        self.data[record.name.value] = record
# Пошук записів за іменем.
    def find(self, name):
        return self.data.get(name)
    
# Видалення записів за іменем.
    def delete(self, name):
        if name in self.data:
            del self.data[name]