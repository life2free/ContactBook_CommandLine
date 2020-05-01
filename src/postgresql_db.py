from peewee import *

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


def initialize_db():
    # initialize contact table
    db.drop_tables([Contact])
    db.create_tables([Contact])

    # insert some data
    justin = Contact(first_name='Justin', last_name='Boet',
                     phone='1234567890', company='Capital one')
    justin.save()
    chris = Contact(first_name='Chris', last_name='Eooo',
                    phone='5000000000', company='Microsoft')
    chris.save()
    stan = Contact(first_name='St', last_name='Leaaa',
                   phone='9680000000', company='Marvel Comic')
    stan.save()
    hattie = Contact(first_name='Haie', last_name='Mosss',
                     phone='3000000003', company='Facebook')
    hattie.save()

    shimin = Contact(first_name='Sin', last_name='Ro',
                     phone='7000000000', company='General Assembly')
    shimin.save()
