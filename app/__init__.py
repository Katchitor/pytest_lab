from flask import Flask

app = Flask(__name__)

app.secret_key = 'super_secret_field_of_dreams_key'

from app import routes
