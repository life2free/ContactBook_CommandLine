from peewee import *
from datetime import date
import re

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
        print(f"\n{self.title}\n")
        self.run()

    def run(self):
        print("Please choice the options as below:")
        print(" 1. Get all contacts.")
        print(" 2. Get contacts by conditions.")
        print(" 3. Create a new contact.")
        print(" 4. Update contact.")
        print(" 5. Delete contact.")
        print(" 6. Exit the app.")
        print()
        try:
            choice = int(input("Please type the option number: "))
            if(choice < 1 or choice > 6):
                self.try_again_with_invalid_input(self.run)
            else:
                if(choice == 1):
                    print("get_all_contacts")
                    self.get_all_contacts()
                if(choice == 2):
                    print("get_contacts")
                    self.get_contacts()
                if(choice == 3):
                    print("create_contact")
                    self.create_contact()
                if(choice == 4):
                    print("4")
                    self.update_contact()
                if(choice == 5):
                    print("delete contact")
                    self.delete_contact()
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
                            self.print_fullname(contact)
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
            if(choice < 1 or choice > 3):
                self.try_again_with_invalid_input(
                    self.get_contacts)
            else:
                if(choice == 1):
                    first_name = input(
                        "Enter first name (or just Press Enter):").strip()
                    last_name = input(
                        "Enter last name (or just Press Enter):").strip()
                    phone = input("Enter phone (or just Press Enter):").strip()
                    company = input(
                        "Enter company (or just Press Enter):").strip()
                    contacts = self.get_contacts_by_conditions(
                        ContactObj(first_name, last_name, phone, company))
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

    def create_contact(self):
        back_to_main = False
        print("Create a new contact\n")
        first_name = input("Enter first name (* required):")
        while(first_name.strip() == ""):
            print(
                "First name is required! If don't want to add a new contact, input back.")
            first_name = input("Enter first name (* required):").strip()
            if(first_name != "" and first_name.lower() == "back"):
                back_to_main = True
                break
        if(back_to_main):
            self.run()
        else:
            last_name = input("Enter last name (* required):").strip()
            while(last_name == ""):
                print(
                    "Last name is required! If don't want to add a new contact, input back.")
                last_name = input("Enter last name (* required):").strip()
                if(last_name != "" and last_name.lower() == "back"):
                    back_to_main = True
                    break
            if(back_to_main):
                self.run()
            else:
                phone = input(
                    "Enter phone (nine digits and first one is no-zero, or just Press Enter):").strip()
                if(phone != ""):
                    while(not self.validate_phone_number(phone)):
                        print(
                            "The number is invalid! If don't want to add a new contact, input back.")
                        phone = input(
                            "Enter phone (nine digits and first one is no-zero, or just Press Enter):").strip()
                        if(phone != "" and phone.lower() == "back"):
                            back_to_main = True
                            break
                if(back_to_main):
                    self.run()
                else:
                    company = input("Enter company (or just Press Enter):")
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
        print(" 1. Get contact by firstname,lastname,phone,company.")
        print(" 2. Back to main options.")
        print(" 3. Exit the app.")
        try:
            choice = int(input("Please type the option number: "))
            if(choice < 1 or choice > 3):
                self.try_again_with_invalid_input(
                    self.update_contact)
            else:
                if(choice == 1):
                    print("Please enter the condition.")
                    first_name = input(
                        "Enter first name (or just Press Enter):").strip()
                    last_name = input(
                        "Enter last name (or just Press Enter):").strip()
                    phone = input("Enter phone (or just Press Enter):").strip()
                    company = input(
                        "Enter company (or just Press Enter):").strip()
                    contacts = self.get_contacts_by_conditions(
                        ContactObj(first_name, last_name, phone, company))
                    length_contacts = len(contacts)
                    if(length_contacts > 0):
                        print("The search result:")
                        self.print_contacts_with_seqno(contacts)
                        print(
                            "Enter the index number of contact you want update.")
                        update_choice = input("Please enter:").strip()

                        if(update_choice != ""):
                            try:
                                update_choice_seqno = int(update_choice)
                                if(update_choice_seqno < 1 or update_choice_seqno > length_contacts):
                                    self.try_again_with_invalid_input(
                                        self.update_contact)
                                else:
                                    print("ready to update")
                                    contact = contacts[update_choice_seqno-1]
                                    print(
                                        f"Original first name: {contact.first_name}")
                                    update_first_name = input(
                                        "Enter first name (* required): ")
                                    print(
                                        f"Original first name: {contact.last_name}")
                                    update_last_name = input(
                                        "Enter last name (* required): ")
                                    print(
                                        f"Original phone: {contact.phone}")
                                    update_phone = input(
                                        "Enter phone: ")
                                    print(
                                        f"Original first name: {contact.company}")
                                    update_company = input(
                                        "Enter company: ")
                                    if(self.confirm_before_update()):
                                        print("confirm to update")
                                        self.update_contact_exec(contact.id, ContactObj(
                                            update_first_name, update_last_name, update_phone, update_company))
                                    '''
                                    if(self.confirm_before_delete()):
                                        contact = contacts[delete_choice_seqno-1]
                                        self.delete_contacts([contact])
                                    '''
                            except ValueError as e:
                                self.try_again_with_invalid_input(
                                    self.update_contact)
                    else:
                        print("No result")
                    self.back_to_main()

                if(choice == 2):
                    print("2")
                    self.back_to_main()
                if(choice == 3):
                    print("Exit the app!")
        except ValueError as e:
            self.try_again_with_invalid_input(self.delete_contact)

    def update_contact_exec(self, contact_id, update_contact):
        print(contact_id)
        Contact.update(first_name=update_contact.first_name, last_name=update_contact.last_name,
                       phone=update_contact.phone, company=update_contact.company).where(Contact.id == contact_id).execute()
        print("The following contact has been updated success. ")
        updated_contact = Contact.get(Contact.id == contact_id)
        self.print_detail_info(updated_contact)

    def confirm_before_update(self):
        update_confirm = input(
            "Are you sure you want to update? y or n: ").strip()
        if update_confirm.lower() == "y":
            return True
        else:
            return False

    def delete_contact(self):
        print(
            "Please choice the conditions as below to get the contacts you want to delete:")
        print(" 1. Get contact by firstname,lastname,phone,company.")
        print(" 2. Back to main options.")
        print(" 3. Exit the app.")
        try:
            choice = int(input("Please type the option number: "))
            if(choice < 1 or choice > 3):
                self.try_again_with_invalid_input(
                    self.delete_contact)
            else:
                if(choice == 1):
                    print("Please enter the condition.")
                    first_name = input(
                        "Enter first name (or just Press Enter):").strip()
                    last_name = input(
                        "Enter last name (or just Press Enter):").strip()
                    phone = input("Enter phone (or just Press Enter):").strip()
                    company = input(
                        "Enter company (or just Press Enter):").strip()
                    contacts = self.get_contacts_by_conditions(
                        ContactObj(first_name, last_name, phone, company))
                    length_contacts = len(contacts)
                    if(length_contacts > 0):
                        print("The search result:")
                        self.print_contacts_with_seqno(contacts)
                        print(
                            "Enter the index number of contact you want delete or Enter all to delete all of the result.")
                        delete_choice = input("Please enter:").strip()

                        if(delete_choice != ""):
                            if(delete_choice.lower() == "all"):
                                if(self.confirm_before_delete()):
                                    self.delete_contacts_exec(contacts)
                            else:
                                try:
                                    delete_choice_seqno = int(delete_choice)
                                    if(delete_choice_seqno < 1 or delete_choice_seqno > length_contacts):
                                        self.try_again_with_invalid_input(
                                            self.delete_contact)
                                    else:
                                        if(self.confirm_before_delete()):
                                            contact = contacts[delete_choice_seqno-1]
                                            self.delete_contacts_exec(
                                                [contact])
                                except ValueError as e:
                                    self.try_again_with_invalid_input(
                                        self.delete_contact)
                    else:
                        print("No result")
                    self.back_to_main()

                if(choice == 2):
                    print("2")
                    self.back_to_main()
                if(choice == 3):
                    print("Exit the app!")
        except ValueError as e:
            self.try_again_with_invalid_input(self.delete_contact)

    def delete_contacts_exec(self, contacts):
        contacts_id_list = []
        for contact in contacts:
            contacts_id_list.append(contact.id)
        print(contacts_id_list)
        Contact.delete().where(Contact.id.in_(contacts_id_list)).execute()
        print("The following contacts has been deleted success. ")
        self.print_contacts(contacts)

    def confirm_before_delete(self):
        delete_confirm = input(
            "Are you sure you want to delete? y or n: ").strip()
        if delete_confirm.lower() == "y":
            return True
        else:
            return False

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
            self.print_detail_info_in_list(contact)

    def print_contacts_with_seqno(self, contacts):
        print("     Name            Phone           Company")
        count = 0
        for contact in contacts:
            count += 1
            self.print_detail_info_in_list_with_seqno(
                contact, count)

    def print_fullname(self, contact):
        print(f"    {contact.first_name} {contact.last_name}")

    def print_detail_info_in_list(self, contact):
        print(
            f"  {contact.first_name} {contact.last_name}        {contact.phone}         {contact.company}")

    def print_detail_info_in_list_with_seqno(self, contact, seqno):
        print(
            f"  {seqno}.  {contact.first_name} {contact.last_name}        {contact.phone}         {contact.company}")

    def print_detail_info(self, contact):
        print(f"    First name: {contact.first_name}")
        print(f"    Last name: {contact.last_name}")
        print(f"    Phone: {contact.phone}")
        print(f"    Company: {contact.company}")

    def validate_phone_number(self, phone_number):
        if(len(phone_number) > 9):
            print("The lenght of number exceeds nine.")
            return False
        ret = re.match(r"^[1-9]\d{8}$", phone_number)
        if(not ret):
            return False
        return True


contact_book = Main()
contact_book.start()
