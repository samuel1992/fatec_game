import json

from game.models import Book, User
# to run this script you must have an user created

BOOKS_FILE = 'books.json'


def load_json_to_dict(local_file):
    with open(local_file) as myfile:
        return json.load(myfile)


if __name__ == '__main__':
    books = load_json_to_dict(BOOKS_FILE)
    for book in books:
        b = Book(**book)
        b.user = User.objects.first()
        b.save()
