from peewee import *
from flask_login import UserMixin
from werkzeug import security
from app.models.core import Base

class UserAlreadyExists(BaseException):
	pass

class User(Base, UserMixin):
    '''
    User model that represnts all user types in the app
    used for authentcation and authorization
    Note: should only contain methods and fields
          related to this functionalties only
    '''
    email = TextField(primary_key=True)
    password = TextField()

    @staticmethod
    def register(email, password):
        password = security.generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
        try:
            user = User.get(email=email)
            raise UserAlreadyExists
        except User.DoesNotExist:
            user = User.create(email=email, password=password)
            return user

    @staticmethod
    def authenticat(email, password):
        user = User.get(email=email)
        check = security.check_password_hash(user.password, password)
        if check:
            return user
        else:
            return False

	def get_id(self):
            return self.email
