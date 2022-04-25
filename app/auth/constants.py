from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')
ALGORITHM = env.str('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES')
