from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        print(value)
        if not self.validate(value):
            raise ValueError("Клас для зберігання номера телефону. Має валідацію формату (12 цифр)")
        else:
            value = self.fromater(value)
            print("Test")
            print(value)
        super().__init__(value)

    @staticmethod
    def fromater(phone):
       
        if len(phone) == 10:
            phone = '38'+phone
            print(phone)
        elif len(phone) != 12:
            raise ValueError("Щось пішло не так")
        
        return phone

    @staticmethod
    def validate(phone):
        if not phone.isdigit():
            return False
        isShortFormat = len(phone) == 10 and phone.startswith('0')
        isLongFormat = phone.startswith('380') and len(phone) == 12

        return isShortFormat or isLongFormat


class Birthday(Field):
    def __init__(self, value):
        self.value = self.validate(value)
        
    @staticmethod
    def validate(birthday):
        try:
            return datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
    
    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self, days=7):
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                delta = (birthday_this_year - today).days
                if 0 <= delta < days:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays
