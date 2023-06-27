from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value.isnumeric():
            self.__value = value
        else:
            raise Exception("Номер телефону має складатися з цифр!")

    def __repr__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        date_list = [int(i) for i in value.split(".")]
        current_datetime = datetime.now()
        if len(date_list) != 3:
            raise Exception("Неправильний формат введення дати!")
        elif date_list[1] > 12:
            raise Exception("Некоректний номер місяця!")
        elif date_list[0] > 31 or (date_list[0] > 30 and date_list[1] in [4, 6, 9, 11]) or (date_list[0] > 29 and date_list[1] == 2):
            raise Exception("Некоректний номер дня!")
        elif int(current_datetime.year) - date_list[2] < 18:
            raise Exception("Некоректний рік народження!")
        else:
            self.__value = value


class Record:
    def __init__(self, name: Name, phone=None, birthday=None):
        self.phones = []
        self.name = name
        self.birthday = birthday
        if phone:
            self.add_phone(phone)

    def __repr__(self):
        if self.phones:
            phones = ""
            for i in range(len(self.phones)):
                if i != 0:
                    phones = phones + ", " + self.phones[i].value
                else:
                    phones = phones + self.phones[i].value
        else:
            phones = "Не вказано"
        if self.birthday:
            birthday = self.birthday.value
        else:
            birthday = "Не вказано"
        return f"Ім'я: {self.name.value}   Телефони: {phones}   День народження: {birthday}"

    def add_phone(self,  phone):
        self.phones.append(phone)
        if self.phones[0] == None:
            del self.phones[0]

    def del_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                self.phones.remove(el)

    def cha_phone(self, phone, new_phone):
        for el in self.phones:
            if el.value == phone:
                el.value = new_phone

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now()
            bd_list = [int(i) for i in self.birthday.value.split(".")]
            bd_date = datetime(
                day=bd_list[0], month=bd_list[1], year=current_datetime.year)
            if bd_date < current_datetime:
                bd_date = datetime(
                    day=bd_list[0], month=bd_list[1], year=current_datetime.year+1)
            days_to_bd = bd_date - current_datetime
            return days_to_bd.days + 1


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data.update({record.name.value: record})

    def iterator(self, N):
        self.N = N
        len_ab = len(self.data)
        records = list(self.data.values())
        k = 0
        while True:
            if 0 < len_ab <= self.N:
                for i in range(k, len(records)):
                    print(f"{records[i]}")
                print('-------')
                break
            elif len_ab <= 0:
                break
            else:
                for i in range(k, k+self.N):
                    print(f"{records[i]}")
                print('-------')
                len_ab -= self.N
                k += N


if __name__ == "__main__":

    name = Name('Bill')
    phone = Phone('1234567890')
    birthday = Birthday("31.08.1996")
    rec = Record(name, phone, birthday)
    rec.add_phone(Phone("0987654321"))
    name = Name('Bill1')
    phone = Phone('1234567890')
    birthday = Birthday("01.07.1976")
    rec1 = Record(name, phone, birthday)
    name = Name('Bill2')
    phone = Phone('1234567890')
    birthday = Birthday("25.04.2000")
    rec2 = Record(name, phone, birthday)
    name = Name('Bill3')
    phone = Phone('123456890')
    birthday = Birthday("28.02.1989")
    rec3 = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec1)
    ab.add_record(rec2)
    ab.add_record(rec3)
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert isinstance(ab['Bill'].birthday, Birthday)
    assert ab['Bill'].phones[0].value == '1234567890'
    print('All Ok)')
    ab.iterator(2)
