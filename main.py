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



def searching_publisher_name():
    query_join1 = session.query(Sale).join(Stock).join(Book).join(Publisher)
    query_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    query_publisher_name = input('Введите имя (name) издателя: ')
    query_result = query_join.filter(Publisher.name == query_publisher_name)
    query_result1 = query_join1.filter(Publisher.name == query_publisher_name)
    for result in query_result.all():
        print(f'Издатель "{query_publisher_name}" найден в магазине "{result.name}" с идентификатором {result.id}')
        for result in query_result1.all():
            print(f'Книга была куплена "{result.date_sale}", за "{result.price}"')


def searching_publisher_id():
    query_join1 = session.query(Sale).join(Stock).join(Book).join(Publisher)
    query_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    query_publisher_name = input('Введите имя (name) издателя: ')
    query_result = query_join.filter(Publisher.id == query_publisher_name)
    query_result1 = query_join1.filter(Publisher.id == query_publisher_name)
    for result in query_result.all():
        print(f'Издатель "{query_publisher_name}" найден в магазине "{result.name}" с идентификатором {result.id}')
        for result in query_result1.all():
            print(f'Книга была куплена "{result.date_sale}", за "{result.price}"')


if __name__ == '__main__':
    searching_publisher_name()
    searching_publisher_id()




session.close()

