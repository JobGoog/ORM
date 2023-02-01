import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale


DSN = 'postgresql://postgres:ipad4ilove@localhost:5432/orm_py'
engine =  sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publ_name = input('Ведите имя писателя или id для вывода: ')


if publ_name.isnumeric():
    for c in session.query(Book).filter(Book.id_publisher == int(publ_name)).all():
        pass
    for v in session.query(Stock).join(Book.stock).filter(Stock.id_book == str(c)).all():
        pass


    print(f'{c} | {v}')
    print(f'{c} |')
else:
    for c in session.query(Publisher).filter(Publisher.name.like(f'%{publ_name}%')).all():
        print()

session.close()

