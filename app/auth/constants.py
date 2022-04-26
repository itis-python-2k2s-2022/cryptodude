from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")

# TODO БД
# this won't work for now
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_SERVER = env.str("DB_SERVER")
DB_NAME = env.str("DB_NAME")
