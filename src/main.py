from peewee import *
from datetime import date

db = PostgresqlDatabase('contacts', user='postgres', password='',
                        host='localhost', port=5432)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Contact(BaseModel):
    first_name = CharField(null=False)
    last_name = CharField(null=False)
    phone = CharField(max_length=10)
    company = CharField()


db.drop_tables([Contact])
db.create_tables([Contact])


# initionalizate some data
justin = Contact(first_name='Justin', last_name='Ber',
                 phone='1234567890', company='Capital one')
justin.save()
chris = Contact(first_name='Chris', last_name='Evans',
                phone='5516785403', company='Microsoft')
chris.save()
stan = Contact(first_name='Stan', last_name='Lee',
               phone='7680735403', company='Marvel Comic')
stan.save()
hattie = Contact(first_name='Hattie', last_name='Mora',
                 phone='7680735403', company='Facebook')
hattie.save()

roger = Contact(first_name='Roger', last_name='Campbell',
                phone='7000302403', company='General Assembly')
roger.save()

noah = Contact(first_name='Noah', last_name='Clark',
               phone='7000380755', company='General Assembly')
noah.save()

shimin = Contact(first_name='Shimin', last_name='Rao',
                 phone='7623735403', company='General Assembly')
shimin.save()


class Condition:
    def __init__(self, first_name, last_name, phone, company):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.company = company


class Main:
    def __init__(self):
        self.title = "Welcome to Contact Book!"

    def start(self):
        print(f"\n{self.title}\n")
        self.run()

    def run(self):
        print("Please choice the options as below:")
        print(" 1. Get all contacts.")
        print(" 2. Get contacts by conditions.")
        print(" 3. Create a new contact.")
        print(" 4. Update a contact.")
        print(" 5. Delete a contact.")
        print(" 6. Exit the app.")
        print()
        try:
            choice = int(input("Please type the option number: "))
            if(choice < 1 or choice > 6):
                self.try_again_with_invalid_input(self.run)
            else:
                if(choice == 1):
                    print("1")
                    self.get_all_contacts()
                if(choice == 2):
                    print("2")
                    self.get_contacts()
                if(choice == 3):
                    print("3")
                if(choice == 4):
                    print("4")
                if(choice == 5):
                    print("5")
                if(choice == 6):
                    print("Exit the app!")
        except ValueError as e:
            self.try_again_with_invalid_input(self.run)

    def get_all_contacts(self):
        print("Please choice the options as below:")
        print(" 1. Only list the firstname and lastname.")
        print(" 2. List all of the information.")
        print(" 3. Back to main options.")
        print(" 4. Exit the app.")
        try:
            choice = int(input("Please type the option number: "))
            if(choice < 1 or choice > 4):
                self.try_again_with_invalid_input(self.get_all_contacts)
            else:
                all_contacts = Contact.select()
                if(choice == 1):
                    if(len(all_contacts) > 0):
                        for contact in all_contacts:
                            self.print_name_in_list(contact)
                    else:
                        print("No result")
                    self.back_to_main()
                if(choice == 2):
                    if(len(all_contacts) > 0):
                        self.print_contacts(all_contacts)
                    else:
                        print("No result")
                    self.back_to_main()
                if(choice == 3):
                    print("3")
                    self.back_to_main()
                if(choice == 4):
                    print("Exit the app!")
        except ValueError as e:
            self.try_again_with_invalid_input(self.get_all_contacts)

    def get_contacts(self):
        print("Please choice the conditions as below:")
        print(" 1. Get contacts by firstname,lastname,phone,company.")
        print(" 2. Back to main options.")
        print(" 3. Exit the app.")
        try:
            choice = int(input("Please type the option number: "))
            if(choice < 1 or choice > 7):
                self.try_again_with_invalid_input(
                    self.get_contacts)
            else:
                if(choice == 1):
                    first_name = input(
                        "Enter first name (or just Press Enter):")
                    last_name = input("Enter last name (or just Press Enter):")
                    phone = input("Enter phone (or just Press Enter):")
                    company = input("Enter company (or just Press Enter):")
                    contacts = self.get_contacts_by_conditions(
                        Condition(first_name, last_name, phone, company))
                    if(len(contacts) > 0):
                        self.print_contacts(contacts)
                    else:
                        print("No result")
                    self.back_to_main()

                if(choice == 2):
                    print("2")
                    self.back_to_main()
                if(choice == 3):
                    print("Exit the app!")
        except ValueError as e:
            self.try_again_with_invalid_input(self.get_contacts)

    def get_contacts_by_conditions(self, condition):
        contacts = Contact.select().where(Contact.first_name.contains(condition.first_name) & Contact.last_name.contains(
            condition.last_name) & Contact.phone.contains(condition.phone) & Contact.company.contains(condition.company))
        return contacts

    def try_again_with_invalid_input(self, func):
        input('Invalid input, Press Enter try again.')
        print()
        func()

    def back_to_main(self):
        input("Press Enter to back to main options.")
        print()
        self.run()

    def print_contacts(self, contacts):
        print("     Name            Phone           Company")
        for contact in contacts:
            self.print_detail_in_list(contact)

    def print_name_in_list(self, contact):
        print(f"    {contact.first_name} {contact.last_name}")

    def print_detail_in_list(self, contact):
        print(
            f"  {contact.first_name} {contact.last_name}        {contact.phone}         {contact.company}")


contact_book = Main()
contact_book.start()
