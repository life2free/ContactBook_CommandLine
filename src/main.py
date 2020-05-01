from postgresql_db import *
import re
import sys


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
        # initialize the database
        initialize_db()
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
        choice_input = input("Your choice: ").strip()
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

    # Get all contacts
    def get_all_contacts(self):
        print()
        print("****  Main Menu >> Get All Contacts  ****\n")
        print("Please choice the option as below:")
        print(" 1. Only list the firstname and lastname")
        print(" 2. List all of the information")
        print(" 3. Back to Main Menu")
        print(" 4. Exit the app")
        print()
        choice_input = input("Your choice: ").strip()
        choice = self.validate_option_number(choice_input, 1, 4)
        if(not choice):
            self.try_again_with_invalid_input(self.get_all_contacts)
        else:
            if(choice == 1 or choice == 2):
                # Get all contacts
                all_contacts = Contact.select()
                if(len(all_contacts) > 0):
                    print("Get all contacts as below\n")
                    whole_info = False if choice == 1 else True
                    self.print_contacts(all_contacts, whole_info)
                else:
                    print("No result")
                self.back_to_main()
            if(choice == 3):
                # Back to Main Menu
                self.main()
            if(choice == 4):
                # Exit the app
                self.exit_app()

    # Get contacts by conditions
    def get_contacts(self):
        print()
        print("****  Main Menu >> Get contacts by conditions  ****\n")
        print("Please choice the option as below:")
        print(" 1. Get contacts by firstname, lastname, phone, company")
        print(" 2. Back to Main Menu")
        print(" 3. Exit the app")
        print()
        choice_input = input("Your choice: ").strip()
        choice = self.validate_option_number(choice_input, 1, 3)
        if(not choice):
            self.try_again_with_invalid_input(self.get_contacts)
        else:
            if(choice == 1):
                first_name = input(
                    "Type first name (or just Press Enter): ").strip()
                last_name = input(
                    "Type last name (or just Press Enter): ").strip()
                phone = input("Type phone (or just Press Enter): ").strip()
                company = input(
                    "Type company (or just Press Enter): ").strip()
                # Get contacts by firs_tname, last_name, phone, company
                contacts = self.get_contacts_by_conditions(
                    ContactObj(first_name, last_name, phone, company))
                if(len(contacts) > 0):
                    print("Get contacts as below\n")
                    self.print_contacts(contacts)
                else:
                    print("No result")
                self.back_to_main()
            if(choice == 2):
                # Back to Main Menu
                self.main()
            if(choice == 3):
                # Exit the app
                self.exit_app()

    # Query the database by firs_tname, last_name, phone, company to get contacts
    def get_contacts_by_conditions(self, condition):
        contacts = Contact.select().where(Contact.first_name.contains(condition.first_name) & Contact.last_name.contains(
            condition.last_name) & Contact.phone.contains(condition.phone) & Contact.company.contains(condition.company))
        return contacts

    # Create a new contact
    # The first name and last name are required
    # The phone number can be empty, or must be nine digits with first digit is non-zero
    # You can back to Main Menu by type 'back' before contact be created
    def create_contact(self):
        print()
        print("****  Main Menu >> Create a new contact  ****\n")
        print("Note: You can back to Main Menu by type 'back' before contact be created\n")
        first_name = input("Type first name (* required): ").strip()
        while(first_name == ""):
            print(
                "First name is required! If don't want to add a new contact, input 'back'.\n")
            first_name = input("Type first name (* required): ").strip()
        if(first_name.lower() == "back"):
            self.main()
        else:
            last_name = input("Type last name (* required): ").strip()
            while(last_name == ""):
                print(
                    "Last name is required! If don't want to add a new contact, input 'back'.\n")
                last_name = input("Type last name (* required): ").strip()
            if(last_name.lower() == "back"):
                self.main()
            else:
                phone = input(
                    "Type phone (nine digits with first one is non-zero, or just Press Enter): ").strip()

                while(phone != "" and phone.lower() != "back" and not self.validate_phone_number(phone)):
                    print(
                        "The number is invalid! If don't want to add a new contact, input 'back'.\n")
                    phone = input(
                        "Type phone (nine digits with first one is non-zero, or just Press Enter): ").strip()
                if(phone.lower() == "back"):
                    self.main()
                else:
                    company = input(
                        "Type company (or just Press Enter): ").strip()
                    if(company != "" and company.lower() == "back"):
                        self.main()
                    else:
                        contact = Contact(first_name=first_name,
                                          last_name=last_name, phone=phone, company=company)
                        contact.save()
                        print("\nNew contact has been created!\n")
                        self.print_detail_info(contact)
                        self.back_to_main()

    # Update a contact
    # Step: 1. Get the search result by condition
    #       2. Select a contact from search result
    #       3. Update the selected contact's information
    # When type new information for contact:
    #   The new first name and new last name are required
    #   The new phone number can be empty, or must be nine digits with first digit is non-zero
    #   User can back to Main Menu by type 'back' when typing new information
    def update_contact(self):
        print()
        print("****  Main Menu >> Update a contact  ****\n")
        print("Please choice the option as below:")
        print(
            " 1. Get contact you want to update by firstname, lastname, phone or company")
        print(" 2. Back to Main Menu")
        print(" 3. Exit the app")
        print()
        choice_input = input("Your choice: ").strip()
        choice = self.validate_option_number(choice_input, 1, 3)
        if(not choice):
            self.try_again_with_invalid_input(self.update_contact)
        else:
            if(choice == 1):
                print("Please type the condition.")
                # type the condition to get contacts matched the condition,
                #   then you can chioce one contact to update
                first_name = input(
                    "Type first name (or just Press Enter): ").strip()
                last_name = input(
                    "Type last name (or just Press Enter): ").strip()
                phone = input("Type phone (or just Press Enter): ").strip()
                company = input(
                    "Type company (or just Press Enter): ").strip()
                contacts = self.get_contacts_by_conditions(
                    ContactObj(first_name, last_name, phone, company))
                length_contacts = len(contacts)
                if(length_contacts > 0):
                    print("The search result:\n")
                    self.print_contacts(contacts)
                    print(
                        "\nType the index number of contact you want update.\n")
                    # User choice the index number of contact which is will be updated
                    update_choice = input("Please type: ").strip()
                    if(update_choice != ""):
                        update_choice_seqno = self.validate_option_number(
                            update_choice, 1, length_contacts)
                        if(not update_choice_seqno):
                            self.try_again_with_invalid_input(
                                self.update_contact)
                        else:
                            print(
                                "\nNote: You can back to Main Menu by type 'back' before contact be updated\n")
                            contact = contacts[update_choice_seqno-1]
                            print(
                                f"Original first name: {contact.first_name}")
                            # type new first name
                            update_first_name = input(
                                "Type new first name (* required): ").strip()
                            while(update_first_name == ""):
                                print(
                                    "First name is required! If don't want to update, input 'back'.")
                                update_first_name = input(
                                    "Type new first name (* required): ").strip()
                            if(update_first_name.lower() == "back"):
                                self.main()
                            else:
                                print(
                                    f"\nOriginal last name: {contact.last_name}")
                                # type new last name
                                update_last_name = input(
                                    "Type new last name (* required): ").strip()
                                while(update_last_name == ""):
                                    print(
                                        "Last name is required! If don't want to update, input 'back'.")
                                    update_last_name = input(
                                        "Type new last name (* required): ").strip()
                                if(update_last_name.lower() == "back"):
                                    self.main()
                                else:
                                    print(
                                        f"\nOriginal phone number: {contact.phone}")
                                    # type new phone number
                                    update_phone = input(
                                        "Type new phone number (nine digits with first one is non-zero, or just Press Enter): ")

                                    while(update_phone != "" and update_phone.lower() != "back" and not self.validate_phone_number(update_phone)):
                                        print(
                                            "The number is invalid! If don't want to update, input 'back'.")
                                        update_phone = input(
                                            "Type new phone number (nine digits with first one is non-zero, or just Press Enter): ").strip()
                                    if(update_phone.lower() == "back"):
                                        self.main()
                                    else:
                                        print(
                                            f"\nOriginal company: {contact.company}")
                                        # type new company info
                                        update_company = input(
                                            "Type new company: ")
                                        if(update_company != "" and update_company.lower() == "back"):
                                            self.main()
                                        else:
                                            if(self.confirm_before_update_or_delete("update")):
                                                self.update_contact_exec(contact.id, ContactObj(
                                                    update_first_name, update_last_name, update_phone, update_company))
                                                self.back_to_main()
                                            else:
                                                self.back_to_main()
                    else:
                        self.back_to_main()
                else:
                    print("\nNo contacts matched the condition")
                    self.back_to_main()
            if(choice == 2):
                # Back to Main Menu
                self.main()
            if(choice == 3):
                # Exit the app
                self.exit_app()

    def update_contact_exec(self, contact_id, update_contact):
        Contact.update(first_name=update_contact.first_name, last_name=update_contact.last_name,
                       phone=update_contact.phone, company=update_contact.company).where(Contact.id == contact_id).execute()
        print("The contact has been updated success as following. ")
        updated_contact = Contact.get(Contact.id == contact_id)
        self.print_detail_info(updated_contact)

    # Delete contacts
    # Step: 1. Get the search result by condition
    #       2. Select a contact or all of contacts from search result
    #       3. Delete specific contact or list of contacts selected
    def delete_contacts(self):
        print()
        print("****  Main Menu >> Delete contacts  ****\n")
        print(
            "Please choice the option as below:")
        print(
            " 1. Get contacts you want to delete by firstname, lastname, phone or company")
        print(" 2. Back to Main Menu")
        print(" 3. Exit the app")
        print()
        choice_input = input("Your choice: ").strip()
        choice = self.validate_option_number(choice_input, 1, 3)
        if(not choice):
            self.try_again_with_invalid_input(self.delete_contacts)
        else:
            if(choice == 1):
                print("Please type the conditions.")
                first_name = input(
                    "Type first name (or just Press Enter): ").strip()
                last_name = input(
                    "Type last name (or just Press Enter): ").strip()
                phone = input("Type phone (or just Press Enter): ").strip()
                company = input(
                    "Type company (or just Press Enter): ").strip()
                contacts = self.get_contacts_by_conditions(
                    ContactObj(first_name, last_name, phone, company))
                length_contacts = len(contacts)
                if(length_contacts > 0):
                    print("The search result:\n")
                    self.print_contacts(contacts)
                    print(
                        "\nType the index number of contact you want delete or Type 'all' to delete all of the result.\n")
                    delete_choice = input("Please type: ").strip()

                    if(delete_choice != ""):
                        if(delete_choice.lower() == "all"):
                            print("The contacts you choiced will be deleted:")
                            self.print_contacts(contacts)
                            if(self.confirm_before_update_or_delete("delete")):
                                # Delete all of contacts from search result
                                self.delete_contacts_exec(contacts)
                        else:
                            delete_choice_seqno = self.validate_option_number(
                                delete_choice, 1, length_contacts)
                            if(not delete_choice_seqno):
                                self.try_again_with_invalid_input(
                                    self.delete_contacts)
                            else:
                                contact = contacts[delete_choice_seqno-1]
                                print("The contact you choiced will be deleted:")
                                self.print_contacts([contact])
                                if(self.confirm_before_update_or_delete("delete")):
                                    # Delete the specific contact you selecte from search result
                                    self.delete_contacts_exec([contact])
                else:
                    print("\nNo contacts matched the deleting condition")
                self.back_to_main()
            if(choice == 2):
                # Back to Main Menu
                self.main()
            if(choice == 3):
                # Exit the app
                self.exit_app()

    # Execute the delete operation in database
    def delete_contacts_exec(self, contacts):
        contacts_id_list = []
        for contact in contacts:
            contacts_id_list.append(contact.id)
        Contact.delete().where(Contact.id.in_(contacts_id_list)).execute()
        print("The following contacts has been deleted success. ")
        self.print_contacts(contacts)

    # Ask user to confirm before update or delete contact
    def confirm_before_update_or_delete(self, update_or_delete):
        print()
        confirm = input(
            f"Are you sure you want to {update_or_delete}? y or n: ").strip()
        if confirm.lower() == "y":
            return True
        else:
            return False

    # Handle the logic when input invalid option
    def try_again_with_invalid_input(self, func):
        input('Invalid input, Press Enter to option menu.')
        print()
        func()

    # Back to Main Menu
    def back_to_main(self):
        print()
        input("Press Enter to back to Main Menu")
        self.main()

    # Print the detail information of list of contacts
    # whole_info(bool): the default value is True
    #               True, print all of information of contact, including first_name, last_name, phone, company;
    #               False, only print the the contact's full name (consist of first_name and last_name)
    def print_contacts(self, contacts, whole_info=True):
        seqno = 0
        if(whole_info):
            print("%5s %-20s %-15s %-10s" % (" ", "Name", "Phone", "Company"))
            for contact in contacts:
                seqno += 1
                self.print_detail_info_in_list(contact, seqno)
        else:
            print("         Name")
            for contact in contacts:
                seqno += 1
                self.print_fullname_in_list(contact, seqno)

    # Only print the contact's full name (consist of first_name and last_name)
    def print_fullname_in_list(self, contact, seqno):
        print(f"  {seqno}.  {contact.first_name} {contact.last_name}")

    # Print the detail information in one row, used when printing list of contacts
    def print_detail_info_in_list(self, contact, seqno):
        full_name = contact.first_name + " " + contact.last_name
        print(
            "  %-3d %-20s %-15s %-10s" % (seqno, full_name, contact.phone, contact.company))

    # Print the detail information of contact
    def print_detail_info(self, contact):
        print(f"    First name: {contact.first_name}")
        print(f"    Last name:  {contact.last_name}")
        print(f"    Phone:      {contact.phone}")
        print(f"    Company:    {contact.company}")

    # Validate the option
    # when the option you choice is not exist, return 0, otherwise return the option number
    def validate_option_number(self, option_number, range_floor, range_ceil):
        ret = re.match(r"^[1-9]$", option_number)
        if(not ret):
            return 0
        option = int(option_number)
        if(option < range_floor or option > range_ceil):
            return 0
        return option

    # Validate the phone number
    # the valiable phone number: 9 digits, the first digit is not zero
    def validate_phone_number(self, phone_number):
        if(len(phone_number) > 9):
            print("The lenght of number exceeds nine.")
            return False
        ret = re.match(r"^[1-9]\d{8}$", phone_number)
        if(not ret):
            return False
        return True

    # Exit the app
    def exit_app(self):
        print("Exit the app!")
        sys.exit()


contact_book = Main()
contact_book.start()
