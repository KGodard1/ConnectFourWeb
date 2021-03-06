from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:

	#TESTING = True
	#DEBUG = True
	FLASK_ENV = 'production'
	SECRET_KEY = environ.get('SECRET_KEY')
	print(SECRET_KEY)
