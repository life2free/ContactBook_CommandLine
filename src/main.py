from peewee import *
from datetime import date
import re
import sys

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


class ContactObj:
    def __init__(self, first_name, last_name, phone, company):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.company = company


class Main:
    def __init__(self):
        self.title = "Welcome to Contact Book!"

    def start(self):
        print(f"\n{self.title}")
        self.main()

    def main(self):
        print()
        print("**********   Main Menu   **********\n")
        print("Please choice the option as below:")
        print(" 1. Get all contacts")
        print(" 2. Get contacts by conditions")
        print(" 3. Create a new contact")
        print(" 4. Update a contact")
        print(" 5. Delete contacts")
        print(" 6. Exit the app")
        print()
        choice_input = input("Option number: ").strip()
        choice = self.validate_option_number(choice_input, 1, 6)
        if(not choice):
            self.try_again_with_invalid_input(self.main)
        else:
            if(choice == 1):
                self.get_all_contacts()
            if(choice == 2):
                self.get_contacts()
            if(choice == 3):
                self.create_contact()
            if(choice == 4):
                self.update_contact()
            if(choice == 5):
                self.delete_contacts()
            if(choice == 6):
                self.exit_app()

    def get_all_contacts(self):
        print()
        print("****  Main Menu >> Get All Contacts  ****\n")
        print("Please choice the option as below:")
        print(" 1. Only list the firstname and lastname")
        print(" 2. List all of the information")
        print(" 3. Back to main")
        print(" 4. Exit the app")
        print()
        choice_input = input("Option number: ").strip()
        choice = self.validate_option_number(choice_input, 1, 4)
        if(not choice):
            self.try_again_with_invalid_input(self.get_all_contacts)
        else:
            if(choice == 1 or choice == 2):
                all_contacts = Contact.select()
                if(len(all_contacts) > 0):
                    whole_info = False if choice == 1 else True
                    self.print_contacts(all_contacts, whole_info)
                else:
                    print("No result")
                self.back_to_main()
            if(choice == 3):
                self.main()
            if(choice == 4):
                self.exit_app()

    def get_contacts(self):
        print()
        print("****  Main Menu >> Get contacts by conditions  ****\n")
        print("Please choice the option as below:")
        print(" 1. Get contacts by firstname, lastname, phone, company")
        print(" 2. Back to main")
        print(" 3. Exit the app")
        print()
        choice_input = input("Option number: ").strip()
        choice = self.validate_option_number(choice_input, 1, 3)
        if(not choice):
            self.try_again_with_invalid_input(self.get_contacts)
        else:
            if(choice == 1):
                first_name = input(
                    "Type first name (or just Press Enter):").strip()
                last_name = input(
                    "Type last name (or just Press Enter):").strip()
                phone = input("Type phone (or just Press Enter):").strip()
                company = input(
                    "Type company (or just Press Enter):").strip()
                contacts = self.get_contacts_by_conditions(
                    ContactObj(first_name, last_name, phone, company))
                if(len(contacts) > 0):
                    self.print_contacts(contacts)
                else:
                    print("No result")
                self.back_to_main()
            if(choice == 2):
                self.main()
            if(choice == 3):
                self.exit_app()

    def get_contacts_by_conditions(self, condition):
        contacts = Contact.select().where(Contact.first_name.contains(condition.first_name) & Contact.last_name.contains(
            condition.last_name) & Contact.phone.contains(condition.phone) & Contact.company.contains(condition.company))
        return contacts

    def create_contact(self):
        print()
        print("****  Main Menu >> Create a new contact  ****\n")
        print("Note: you can back to Main Menu by type back before confirm update\n")
        back_to_main = False
        first_name = input("Type first name (* required):").strip()
        while(first_name == ""):
            print(
                "First name is required! If don't want to add a new contact, input back.")
            first_name = input("Type first name (* required):").strip()
        if(first_name.lower() == "back"):
            self.main()
        else:
            last_name = input("Type last name (* required):").strip()
            while(last_name == ""):
                print(
                    "Last name is required! If don't want to add a new contact, input back.")
                last_name = input("Type last name (* required):").strip()
            if(last_name.lower() == "back"):
                self.main()
            else:
                phone = input(
                    "Type phone (nine digits with first one is non-zero, or just Press Enter):").strip()

                while(phone != "" and phone.lower() != "back" and not self.validate_phone_number(phone)):
                    print(
                        "The number is invalid! If don't want to add a new contact, input back.")
                    phone = input(
                        "Type phone (nine digits with first one is non-zero, or just Press Enter):").strip()
                if(phone.lower() == "back"):
                    self.main()
                else:
                    company = input(
                        "Type company (or just Press Enter):").strip()
                    if(company != "" and company.lower() == "back"):
                        self.main()
                    else:
                        contact = Contact(first_name=first_name,
                                          last_name=last_name, phone=phone, company=company)
                        contact.save()
                        print("\nNew contact has been created!\n")
                        self.print_detail_info(contact)
                        self.back_to_main()

    def update_contact(self):
        print("Update contact")
        print(
            "Please choice the conditions as below to get the contact you want to update:")
        print(" 1. Get contact by firstname,lastname,phone,company")
        print(" 2. Back to main")
        print(" 3. Exit the app")
        try:
            choice = int(input("Please type the option number: "))
            if(choice < 1 or choice > 3):
                self.try_again_with_invalid_input(
                    self.update_contact)
            else:
                if(choice == 1):
                    print("Please enter the condition.")
                    first_name = input(
                        "Type first name (or just Press Enter):").strip()
                    last_name = input(
                        "Type last name (or just Press Enter):").strip()
                    phone = input("Type phone (or just Press Enter):").strip()
                    company = input(
                        "Type company (or just Press Enter):").strip()
                    contacts = self.get_contacts_by_conditions(
                        ContactObj(first_name, last_name, phone, company))
                    length_contacts = len(contacts)
                    if(length_contacts > 0):
                        print("The search result:")
                        self.print_contacts(contacts)
                        print(
                            "Type the index number of contact you want update.")
                        update_choice = input("Please enter:").strip()

                        if(update_choice != ""):
                            try:
                                update_choice_seqno = int(update_choice)
                                if(update_choice_seqno < 1 or update_choice_seqno > length_contacts):
                                    self.try_again_with_invalid_input(
                                        self.update_contact)
                                else:
                                    back_to_main = False
                                    print("ready to update")
                                    contact = contacts[update_choice_seqno-1]
                                    print(
                                        f"Original first name: {contact.first_name}")
                                    update_first_name = input(
                                        "Type first name (* required): ").strip()
                                    while(update_first_name == ""):
                                        print(
                                            "First name is required! If don't want to update, input back.")
                                        update_first_name = input(
                                            "Type first name (* required): ").strip()
                                        if(update_first_name != "" and update_first_name.lower() == "back"):
                                            back_to_main = True
                                            break
                                    if(not back_to_main):
                                        print(
                                            f"Original first name: {contact.last_name}")
                                        update_last_name = input(
                                            "Type last name (* required): ").strip()
                                        while(update_last_name == ""):
                                            print(
                                                "Last name is required! If don't want to update, input back.")
                                            update_last_name = input(
                                                "Type last name (* required): ").strip()
                                            if(update_last_name != "" and update_last_name.lower() == "back"):
                                                back_to_main = True
                                                break
                                        if(not back_to_main):
                                            print(
                                                f"Original phone: {contact.phone}")
                                            update_phone = input(
                                                "Type phone (nine digits with first one is non-zero, or just Press Enter): ")
                                            if(update_phone != ""):
                                                while(not self.validate_phone_number(update_phone)):
                                                    print(
                                                        "The number is invalid! If don't want to update, input back.")
                                                    update_phone = input(
                                                        "Type phone (nine digits with first one is non-zero, or just Press Enter): ").strip()
                                                    if(update_phone != "" and update_phone.lower() == "back"):
                                                        back_to_main = True
                                                        break
                                                if(back_to_main):
                                                    self.main()
                                                else:
                                                    print(
                                                        f"Original company: {contact.company}")
                                                    update_company = input(
                                                        "Type company: ")
                                                    if(self.confirm_before_update_or_delete("update")):
                                                        print(
                                                            "confirm to update")
                                                        self.update_contact_exec(contact.id, ContactObj(
                                                            update_first_name, update_last_name, update_phone, update_company))

                            except ValueError as e:
                                self.try_again_with_invalid_input(
                                    self.update_contact)
                    else:
                        print("No result")
                    self.back_to_main()

                if(choice == 2):
                    self.main()
                if(choice == 3):
                    self.exit_app()
        except ValueError as e:
            self.try_again_with_invalid_input(self.delete_contact)

    def update_contact_exec(self, contact_id, update_contact):
        print(contact_id)
        Contact.update(first_name=update_contact.first_name, last_name=update_contact.last_name,
                       phone=update_contact.phone, company=update_contact.company).where(Contact.id == contact_id).execute()
        print("The following contact has been updated success. ")
        updated_contact = Contact.get(Contact.id == contact_id)
        self.print_detail_info(updated_contact)

    def delete_contacts(self):
        print()
        print("****  Main Menu >> Delete contacts  ****\n")
        print(
            "Please choice the option as below to get the contacts you want to delete")
        print(" 1. Get contacts by firstname, lastname, phone, company")
        print(" 2. Back to main")
        print(" 3. Exit the app")
        print()
        choice_input = input("Option number: ").strip()
        choice = self.validate_option_number(choice_input, 1, 3)
        if(not choice):
            self.try_again_with_invalid_input(self.delete_contacts)
        else:
            if(choice == 1):
                print("Please enter the conditions.")
                first_name = input(
                    "Type first name (or just Press Enter):").strip()
                last_name = input(
                    "Type last name (or just Press Enter):").strip()
                phone = input("Type phone (or just Press Enter):").strip()
                company = input(
                    "Type company (or just Press Enter):").strip()
                contacts = self.get_contacts_by_conditions(
                    ContactObj(first_name, last_name, phone, company))
                length_contacts = len(contacts)
                if(length_contacts > 0):
                    print("The search result:")
                    self.print_contacts(contacts)
                    print(
                        "\nType the index number of contact you want delete or Type all to delete all of the result.")
                    delete_choice = input("Please type: ").strip()

                    if(delete_choice != ""):
                        if(delete_choice.lower() == "all"):
                            if(self.confirm_before_update_or_delete("delete")):
                                self.delete_contacts_exec(contacts)
                        else:
                            delete_choice_seqno = self.validate_option_number(
                                delete_choice, 1, length_contacts)
                            if(not delete_choice_seqno):
                                self.try_again_with_invalid_input(
                                    self.delete_contacts)
                            elif(self.confirm_before_update_or_delete("delete")):
                                contact = contacts[delete_choice_seqno-1]
                                self.delete_contacts_exec([contact])
                else:
                    print("No result")
                self.back_to_main()

            if(choice == 2):
                self.main()
            if(choice == 3):
                self.exit_app()

    def delete_contacts_exec(self, contacts):
        contacts_id_list = []
        for contact in contacts:
            contacts_id_list.append(contact.id)
        print(contacts_id_list)
        Contact.delete().where(Contact.id.in_(contacts_id_list)).execute()
        print("The following contacts has been deleted success. ")
        self.print_contacts(contacts)

    def confirm_before_update_or_delete(self, update_or_delete):
        confirm = input(
            f"Are you sure you want to {update_or_delete}? y or n: ").strip()
        if confirm.lower() == "y":
            return True
        else:
            return False

    def try_again_with_invalid_input(self, func):
        input('Invalid input, Press Enter to try again.')
        print()
        func()

    def back_to_main(self):
        print()
        input("Press Enter to back to Main Menu")
        self.main()

    def print_contacts(self, contacts, whole_info=True):
        seqno = 0
        if(whole_info):
            print("         Name            Phone           Company")
            for contact in contacts:
                seqno += 1
                self.print_detail_info_in_list(contact, seqno)
        else:
            print("         Name")
            for contact in contacts:
                seqno += 1
                self.print_fullname_in_list(contact, seqno)

    def print_fullname_in_list(self, contact, seqno):
        print(f"  {seqno}.  {contact.first_name} {contact.last_name}")

    def print_detail_info_in_list(self, contact, seqno):
        print(
            f"  {seqno}.  {contact.first_name} {contact.last_name}        {contact.phone}         {contact.company}")

    def print_detail_info(self, contact):
        print(f"    First name: {contact.first_name}")
        print(f"    Last name: {contact.last_name}")
        print(f"    Phone: {contact.phone}")
        print(f"    Company: {contact.company}")

    def validate_option_number(self, option_number, range_floor, range_ceil):
        ret = re.match(r"^[1-9]$", option_number)
        if(not ret):
            return 0
        option = int(option_number)
        if(option < range_floor or option > range_ceil):
            return 0
        return option

    def validate_phone_number(self, phone_number):
        if(len(phone_number) > 9):
            print("The lenght of number exceeds nine.")
            return False
        ret = re.match(r"^[1-9]\d{8}$", phone_number)
        if(not ret):
            return False
        return True

    def exit_app(self):
        print("Exit the app!")
        sys.exit()


contact_book = Main()
contact_book.start()
