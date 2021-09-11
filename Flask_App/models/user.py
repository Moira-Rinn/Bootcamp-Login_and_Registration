from Flask_App.config.mysql_connection import connectToMySQL
from flask import flash
import re
# from flask_bcrypt import Bcrypt


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls, query, data=None):
        users_from_db = connectToMySQL('users_db').query_db(query, data)
        users = []
        for u in users_from_db:
            users.append(cls(u))
        if users == []:
            return False
        return users

    @classmethod
    def save(cls, data=None):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES(%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"
        user_id = connectToMySQL('users_db').query_db(query, data)
        return user_id

    @staticmethod
    def registration_validation(data):
        is_valid = True
        name_regex = re.compile(r'^[a-zA-Z]')
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['fname']) == 0 or not name_regex.match(data['fname']):
            flash("Please enter a <span>valid first name</span>.")
            is_valid = False
        if len(data['lname']) == 0 or not name_regex.match(data['lname']):
            flash("Please enter a <span>valid last name</span>.")
            is_valid = False
        if len(data['email']) == 0 or not email_regex.match(data['email']):
            flash("Please enter a <span>valid email</span>.")
            is_valid = False
        return is_valid

    # @classmethod
    # def remove_user(cls, query, data=None):
    #     user_id = connectToMySQL('users_db').query_db(query, data)
    #     return user_id

    # @classmethod
    # def edit_user(cls, query, data=None):
    #     user_id = connectToMySQL('users_db').query_db(query, data)
    #     return user_id
