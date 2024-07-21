import mysql.connector as mysql
import random

a = mysql.connect(host='localhost', user='root', passwd='', database='bookcollection')
cursor = a.cursor()

# constants
TABLE_NAME = 'BOOKS'

def add_book(title, author, genre, year, status):
    global cursor


    ## FIX THIS PORTION ##
    cursor.execute(f'select count(book_id) from {TABLE_NAME}');
    book_id = 0
    for m in cursor:
        try int(m):
            book_id = int(m)+1
    cursor.execute(f'insert into books values({int(book_id)}, {title}, {author}, {genre}, {int(year)}, {int(status)})')
    cursor.commit()


def update_book(book_id, new_info):
    # book_id is identifier, new_info is a dictionary of the new information
    global cursor

    for key in new_info.keys():
        value = new_info[key]
        if key in ['year', 'status', 'book_id']:
            value = int(value)
        cursor.execute(f'update {TABLE_NAME} set {key}={value} where book_id={book_id}')
        cursor.commit()

def delete_book(book_id):
    global cursor
    cursor.execute(f'delete from {TABLE_NAME} where book_id={book_id}')

def search_book(info):
    # info will be a dictionary, containing type: value
    global cursor
    k = info.keys()[0]
    v = info[k]
    if k in ['year', 'status', 'book_id']:
        v = int(v)
    cursor.execute(f'select * from {TABLE_NAME} where {k}={v}')
    for m in cursor:
        print(m)

# simple CLI
def main():
    # define the table
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}(book_id INTEGER PRIMARY KEY, title VARCHAR(75) NOT NULL, author VARCHAR(50) NOT NULL, genre VARCHAR(20), year INTEGER, status INTEGER)')
    cursor.commit()
    while True:
        print("1. Add a new book")
        print("2. Update a book")
        print("3. Delete a book")
        print("4. Search for books")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == 1:
            data = input("Enter comma seperated data as title, author, genre, year, status: ")
            title, author, genre, year, status = data.split(',')
            add_book(title, author, genre, year, status)
            print('your book has been added!')
        elif choice == 2:
            book_id = int(input("Enter the book_id: "))
            data = input("Enter new data in the format field1:value1,field2:value2 ....: ")
            t = data.split(',')
            vals = [x.split(':') for x in t]
            d = {}
            for i in range(0, len(vals), 2):
                d[vals[i]] = vals[i+1]
            update_book(book_id, d)
            print('data updated!')
        elif choice == 3:
            book_id = int(input("Enter the book_id: "))
            delete_book(book_id)
            print('book deleted!')
        elif choice == 4:
            data = input("Enter query in the form of field:value -> ")
            t = data.split(':')
            d = {t[0]:t[1]}
            search_book(d)
        
        elif choice == 5:
            print('Thank You! ')


