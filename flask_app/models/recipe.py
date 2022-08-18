from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
import re
from flask_app.models.user import User


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.instructions = data['instructions']
        self.description = data['description']
        self.created_at = data['created_at']
        self.update_at = data['update_at']
        # time to make in minutes (int) 1:less than 30, 0:more than 30
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.user=User.get_by_id(data['user_id'])

    @classmethod
    def create(cls, data):
        mysql = MySQLConnection('recetas')
        query = "INSERT INTO recipies (name,  instructions, description, under30, date_made, user_id) VALUES (%(name)s, %(instructions)s, %(description)s, %(under30)s, %(date_made)s,%(user_id)s)"
        return mysql.query_db(query, data)

    @classmethod
    def get_all(cls):
        mysql = MySQLConnection('recetas')
        query = "SELECT * FROM recipies"
        result = mysql.query_db(query)
        return [cls(i) for i in result]

    @classmethod
    def get_by_id(cls, data):
        mysql = MySQLConnection('recetas')
        data= {"id": data}
        query = "SELECT * FROM recipies WHERE id = %(id)s"
        result = mysql.query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        mysql = MySQLConnection('recetas')
        query = "UPDATE recipies SET name = %(name)s,  instructions = %(instructions)s, description = %(description)s, under30 = %(under30)s, date_made = %(date_made)s WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @classmethod        
    def delete(cls, data):
        mysql = MySQLConnection('recetas')
        data={"id":data}
        query = "DELETE FROM recipies WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @staticmethod
    def validate(data):
        valid = True
        if len(data['name']) < 2:
            valid = False
            flash('name cannot be blank', "recipe_error")
        if len(data['instructions']) < 2:
            valid = False
            flash('Instructions cannot be blank', "recipe_error")
        if len(data['description']) < 2:
            valid = False
            flash('Description cannot be blank', "recipe_error")
        return valid
