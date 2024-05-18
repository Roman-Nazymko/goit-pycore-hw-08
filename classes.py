from collections import UserDict
from datetime import datetime, timedelta

"""Базовий клас для полів запису"""
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

"""Клас для зберігання імені контакту. Обов'язкове поле."""
class Name(Field):
    def __init__(self, name):
          self.value = name

"""Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""
class Phone(Field):
    def __init__(self, phone):
         self.value = self.validate_phone_number(phone)
    
    def validate_phone_number(self, phone):
         if len(phone) != 10:
              raise ValueError("Phone number must be a string of 10 digits.")
         if not phone.isdigit():
              raise ValueError("The phone number must contain only numbers")

         return phone 

"""Клас для зберігання дати народження"""
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

"""Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    #Додавання телефонів
    def add_phone(self, phone):
         self.phones.append(Phone(phone))
    
    #Видалення телефонів
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                print(f"Phone number '{phone}' removed successfully.")
                break
        else:
            print(f"No phone number '{phone}' found.")
    
    #Редагування телефонів
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                print(f"Phone number '{old_phone}' edited successfully to '{new_phone}'.")
                break
            else:
                print(f"No phone number '{old_phone}' found.")

    #Пошук телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return phone
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)     

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    # Додавання записів
    def add_record(self, record):
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    #Пошук записів за іменем
    def find(self, name):
        return self.data.get(name)
    
    #Видалення записів за іменем
    def delete(self, name):
        del self.data[name]
    
    #Отриманння майбутніх днів народження
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        def is_weekend_day(day):
            return day > 4

        for name, record in self.data.items():
            if record.birthday:
                birthday = record.birthday.value.replace(year=today.year).date()

                timedelta_days = (birthday - today).days

                if 0 <= timedelta_days <= 7:
                    if is_weekend_day(birthday.weekday()):
                        days_delta = 2 if birthday.weekday() == 5 else 1
                        congratulation_date = birthday + timedelta(days=days_delta)
                    else:
                        congratulation_date = birthday

                    upcoming_birthdays.append(
                        {
                            "name": name,
                            "congratulation_date": congratulation_date.strftime(
                                "%d.%m.%Y"
                            ),
                        }
                    )

        return upcoming_birthdays