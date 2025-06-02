from hashlib import scrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
mail = Mail()
bcrypt = Bcrypt()
serializer = None 
db = SQLAlchemy()