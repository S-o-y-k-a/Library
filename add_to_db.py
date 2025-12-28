import requests
import random
import string
from datetime import date, timedelta

books = 600
readers = 200
issuances = 450

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

book_ids = []

print("creating books...")
for i in range(books):
    book_data = {
        "name": random_string(10),
        "author": random_string(8),
        "theme": random_string(6),
        "publisher": random_string(6)
    }
    response = requests.post("http://127.0.0.1:8000/books/", json=book_data)
    if response.status_code == 200:
        book_ids.append(response.json()["book_id"])
    else:
        print("Can't create book:", response.text)

reader_ids = []

print("creating readers...")
for i in range(readers):
    reader_data = {
        "passport_number": str(random.randint(1000000, 9999999)),
        "name": random_string(6),
        "address": random_string(25),
        "phone_number": f"+374{random.randint(10000000, 99999999)}",
        "mark": str(date.today() - timedelta(days=random.randint(0, 365*5)))
    }
    response = requests.post("http://127.0.0.1:8000/readers/", json=reader_data)
    if response.status_code == 200:
        reader_ids.append(response.json()["reader_id"])
    else:
        print("Can't create reader:", response.text)

print("creating issuances...")
for i in range(issuances):
    issuance_data = {
        "issuance_date": str(date.today() - timedelta(days=random.randint(0, 365*5))),
        "date_of_actual_return": str(date.today() - timedelta(days=random.randint(0, 365*5))),
        "book_id": random.choice(book_ids),
        "reader_id": random.choice(reader_ids)
    }
    response = requests.post("http://127.0.0.1:8000/issuances/", json=issuance_data)
    if response.status_code != 200:
        print("Can't create issuance:", response.text)

print("Added things to database!")