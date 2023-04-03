from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from pprint import pprint

DATABASE = 'books'

class book:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = data['user_id']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO books (title,description,user_id) VALUES (%(title)s,%(description)s,%(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT books.*,users.first_name,users.last_name FROM books LEFT JOIN users on users.id=books.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        # results will be a list of dictionaries
        books = []
        for dictionary in results:
            # dictionary is a dictionary in the list
            books.append( cls(dictionary) )
            # adding an instance of the book class to the books list
        return books

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all_with_user(cls) -> list:
        query = "SELECT * FROM books JOIN users ON users.id = books.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        # results will be a list of dictionaries
        books = []
        for dictionary in results:
            # dictionary is a dictionary in the list
            books.append( cls(dictionary) )
            # adding an instance of the book class to the books list
        pprint(books[0].first_name)
        return books
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT books.*,users.first_name,users.last_name FROM books LEFT JOIN users on users.id=books.user_id WHERE books.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])


    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! VALIDATIONS
    @staticmethod
    def validate_book(book:dict) -> bool:
        is_valid = True # we assume this is true
        if len(book['title']) < 2:
            flash("Requirements not met")
            is_valid = False
        if len(book['description']) < 10:
            flash("Requirements not met")
            is_valid = False
        return is_valid