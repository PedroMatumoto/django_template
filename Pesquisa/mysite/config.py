from decouple import config 

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')

DB_NAME = config('DB_NAME')
DB_HOST = config('DB_HOST')
DB_PASSWORD = config('DB_PASSWORD')
DB_PORT = config('DB_PORT')
DB_USER = config('DB_USER')
