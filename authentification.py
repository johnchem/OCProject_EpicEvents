import functools
from sqlalchemy import event
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User
# from settings import EXPIRATION_TIME_TOKEN
from settings import PRIVATE_KEY, PUBLIC_KEY, EXPIRATION_TIME_TOKEN



def authenticate_user(user, password):
    if check_password_hash(user.password, password):
        return user.id
    return None


@event.listens_for(User.password, "set", retval=True)
# @event.listens_for(User.password, "modified", retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


# Fonction pour générer un token JWT
def encode(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(EXPIRATION_TIME_TOKEN))
    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')


# Fonction pour vérifier un token JWT
def decode(token):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
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



if __name__ == '__main__':
    action = input("Voulez-vous vous inscrire (i), vous authentifier (a), générer (g) ou vérifier (v) un JWT ? ")

    if action == 'i':
        username = input("Entrez votre nom d'utilisateur : ")
        password = input("Entrez votre mot de passe : ")
        register_user(username, password)
        print("Utilisateur enregistré avec succès.")
    elif action == 'a':
        username = input("Entrez votre nom d'utilisateur : ")
        password = input("Entrez votre mot de passe : ")
        user_id = authenticate_user(username, password)
        if user_id:
            print(f"Authentification réussie pour l'utilisateur avec l'ID : {user_id}")
        else:
            print("Authentification échouée.")
    elif action == 'g':
        user_id = input("Entrez l'ID de l'utilisateur : ")
        token = generate_jwt({'user_id': user_id})
        print(f"Token JWT généré : {token}")
    elif action == 'v':
        token = input("Entrez le token JWT à vérifier : ")
        result = verify_jwt(token)
        print(f"Résultat de la vérification : {result}")
    else:
        print("Action invalide.")

