from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint
from flask_app.models.book import book


DATABASE = 'books'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.books = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    ## ! used in user validation
    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one_with_books(cls, data):
        query = "SELECT * FROM users LEFT JOIN books ON users.id = books.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        pprint(results)
        user = cls(results[0])
        for user_dict in results:
            book_data = {
                'id': user_dict['books.id'],
                'title': user_dict['title'],
                'description': user_dict['description'],
                'user_id': user_dict['user_id'],
                'created_at': user_dict['books.created_at'],
                'updated_at': user_dict['books.updated_at']
            }
            user.books.append(book(book_data))
        return user
    
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)


    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(user['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(user['password']) != 8:
            flash("password must be 8 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if user['password'] != user['confirm-password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(books:dict) -> bool:
        is_valid = True # we assume this is true
        if len(books['first_name']) < 3:
            flash("Requirements not met")
            is_valid = False
        if len(books['last_name']) < 3:
            flash("Requirements not met")
            is_valid = False
        if not EMAIL_REGEX.match(books['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid