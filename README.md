# Contact Book

A Contact Book builded with Python and SQL.

## Description:

This command line application -- Contact Book is a full CRUD capability application builded with python and SQL database (PostgreSQL). In this application, users are able to create new contacts, update and delete contacts. They also be able to see a list of contacts in their contact book. They are be able to find a contact or list of contacts by the contact's first name, last name, phone or company.

## Technologies Used

- Python3
- PostgreSQL
- Peewee
- pyscopg2
- pipenv

## Instructions

Here's the instuctions how to install and use it.

### Install

1. Make a new directory or go into a directory
2. In the directory, Fork and clone the repository
3. Go into the src dir
4. Run `psql < settings.sql`
   - This command will create a postgerSQL database named contacts on your computer
5. Run `pipenv install peewee psycopg2 autopep8`
   - This command will install the dependencies packages
6. Run `pipenv shell` to Start your virtual environment
7. Run `python3 main.py` to experience this command line application

### Usage

The usage show how to navigate through the application. In this application, user can view, create, update, delete the contact. There are some options for user to choice.

#### View Contact

There are two options to get the contacts list to view the contact information.

1. Get all of the contact  
   Select this option, user can view all of contacts. There are two display option.
   - Only list the first name and last name  
     Only display each contact's full name (consist of first name and last name)
   - List all of the information  
     Display all of information of each contact, including first name, last name, phone, company;
2. Get contacts by conditions  
   Select this option, user can type the first name, last name, phone number or company to search contacts. The application apply fuzzy search to search contacts from database.

#### Create Contact

1. Create a new contact  
   Select this option, user can create a new contact. When creating a new contact:
   - The first name and last name are required
   - The phone number can be empty, or must be ten digits with first digit is non-zero
   - User can back to Main Menu by type 'back' before contact be created

#### Update Contact

1. Update a contact  
   Select this option, user can update a existed contact. If want to update a existed contact, there are some step:
   1. Get list of contacts by condition  
      Type the conditions ( first name, last name, phone number or company ) to get list of contacts
   2. Select a contact from search result  
      Select a specific contact which is will be updated
   3. Update the selected contact's information  
      Type the new information for the contact. When type new information for contact:
   - The new first name and new last name are required
   - The new phone number can be empty, or must be ten digits with first digit is non-zero
   - User can back to Main Menu by type 'back' when typing new information

#### Delete Contact

1. Delete contacts  
   Select this option, user can update one existed contact or list of contacts. If want to delete contacts, there are some step:
   1. Get list of contacts by condition  
      Type the conditions ( first name, last name, phone number or company ) to get list of contacts
   2. Select a contact or all of contacts from search result  
      Select a specific contact or all of contacts from search result for deleting.
   3. Delete specific contact or list of contacts selected

#### Exit the app

User can exit the applicaton when choicing this option.

## Contribute

- Source code: https://github.com/life2free/ContactBook_CommandLine
- Issue Tracker: https://github.com/life2free/ContactBook_CommandLine/issues
