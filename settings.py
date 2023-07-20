import environ
import os

env = environ.Env()

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Take environment variables from .env file
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env'),
    overwrite=True
    )

# postgres CLI link
PSQL = env("PSQL")

SERVER = env("SERVER")
DATABASE_NAME = env("DATABASE_NAME")

# Connection option
PORT = env("PORT")

# Admin credential
ADMIN_LOGIN = env("ADMIN_LOGIN")
PGPASSWORD = env("PGPASSWORD")  # permet de stocker le mdp admin dans les variables d'env

# Application credential
LOGIN = env("DATABASE_LOGIN")
PWD = env("DATABASE_PWD")
