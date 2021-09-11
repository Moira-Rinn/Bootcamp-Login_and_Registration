from Flask_App.config.mysql_connection import connectToMySQL
from flask import flash
# from flask_bcrypt import Bcrypt
import re


class Login:
    def __init__(self, data):
        self.id = data['id']
        self.pass1 = data['pass1']
        self.pass2 = data['pass2']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls, query, data=None):
        logins_from_db = connectToMySQL('users_db').query_db(query, data)
        logins = []
        for login in logins_from_db:
            logins.append(cls(login))
        if logins == []:
            return False
        return logins

    @classmethod
    def save(cls, data=None):
        query = "INSERT INTO logins (pass1, pass2, user_id, created_at, updated_at) VALUES (%(pass1)s, %(pass2)s, %(user_id)s, NOW(), NOW());"
        login_id = connectToMySQL('users_db').query_db(query, data)
        return login_id

    @staticmethod
    def password_validation(data):
        is_valid = True
        pass_regex = re.compile(r'^[a-zA-Z0-9.+_\-*!#@&$%]')
        if data['pass1'] != data['pass2']:
            flash("Passwords do <span>not</span> match.")
            is_valid = False
        if len(data['pass1']) < 6 or len(data['pass1']) > 100 or not pass_regex.match(data['pass1']):
            flash("Password must be at least <span>6 characters</span> long.")
            is_valid = False
        return is_valid
