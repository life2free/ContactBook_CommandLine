from peewee import *
from datetime import date

db = PostgresqlDatabase('contacts', user='postgres', password='',
                        host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Contact(BaseModel):
    first_name = CharField()
    last_name = CharField()
    phone = CharField(max_length=10)
    company = CharField()


db.connect()
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
