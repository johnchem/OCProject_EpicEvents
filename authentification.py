import functools
import os
from sentry_sdk import capture_exception
from sqlalchemy import event
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User

# from settings import EXPIRATION_TIME_TOKEN
from settings import PRIVATE_KEY, PUBLIC_KEY, EXPIRATION_TIME_TOKEN, TOKEN_FILE


def authenticate_user(user, password):
    try:
        if check_password_hash(user.password, password):
            # return user.id
            return True
        return False
    except Exception as err:
        capture_exception(err)
        return False


@event.listens_for(User.password, "set", retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


# Fonction pour générer un token JWT
def encode(payload):
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(EXPIRATION_TIME_TOKEN))
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


# Fonction pour vérifier un token JWT
def decode(token):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Le token a expiré."
    except jwt.InvalidTokenError:
        return "Token invalide."


def encode_decode_jwt(function):
    @functools.wraps(function)
    def inner(self, token=None, *args, **kwargs):
        if token:
            decoded_data = decode(token)
            data = function(self, decoded_data, *args, **kwargs)
        else:
            data = function(self, *args, **kwargs)
        token = encode(data)
        return token

    return inner


# Fonction pour créer un token JWT pour un utilisateur authentifié
def create_id_token(user):
    payload = {
        "user": user.email,
    }
    token = encode(payload)
    return token


# Fonction pour vérifier le token JWT reçu du client
def verify_jwt_token(token):
    try:
        payload = decode(token)
        user = payload.get("user")
        expiration = payload.get("exp")

        # Vérification de l'expiration
        if datetime.datetime.fromtimestamp(expiration) < datetime.datetime.utcnow():
            return None, "expired token"

        return user, None  # Utilisateur authentifié

    except jwt.ExpiredSignatureError:
        return None, "expired token"
    except jwt.InvalidTokenError:
        return None, "invalid token"


# Fonction pour enregistrer le token dans un fichier local
def save_token_to_file(token):
    with open(TOKEN_FILE, "w") as file:
        file.write(token)


# Fonction pour lire le token depuis le fichier local
def read_token_from_file():
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            token = file.read()
        return token
    else:
        return None


def remove_token_file():
    if os.path.isfile(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    else:
        print(f"Error: {TOKEN_FILE} file not found")


if __name__ == "__main__":
    pass
