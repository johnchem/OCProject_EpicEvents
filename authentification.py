from sqlalchemy import event
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from settings import SECRET_KEY

# # Fonction pour enregistrer un nouvel utilisateur
# def register_user(username, password):
#     hashed_password = generate_password_hash(password)
#     new_user = User(username=username, password=hashed_password)
#     session.add(new_user)
#     session.commit()


# Fonction pour authentifier un utilisateur
def authenticate_user(user, password):
    if check_password_hash(user.password, password):
        return user.id
    return None


@event.listens_for(User.password, "set", retval=True)
@event.listens_for(User.password, "modified", retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


# Fonction pour générer un token JWT
def generate_jwt(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


# Fonction pour vérifier un token JWT
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "Le token a expiré."
    except jwt.InvalidTokenError:
        return "Token invalide."

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String, unique=True)
#     password = Column(String)

# # Créer la base de données SQLite en mémoire (vous pouvez choisir un emplacement de fichier différent)
# engine = create_engine('sqlite:///jwt_auth.db')

# # Créer les tables dans la base de données
# Base.metadata.create_all(engine)

# # Créer une session SQLAlchemy
# Session = sessionmaker(bind=engine)
# session = Session()



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

# if __name__ == '__main__':
#     action = input("Voulez-vous générer (g) ou vérifier (v) un JWT ? ")
    
#     if action == 'g':
#         user_id = input("Entrez l'ID de l'utilisateur : ")
#         token = generate_jwt({'user_id': user_id})
#         print(f"Token JWT généré : {token}")
#     elif action == 'v':
#         token = input("Entrez le token JWT à vérifier : ")
#         result = verify_jwt(token)
#         print(f"Résultat de la vérification : {result}")
#     else:
#         print("Action invalide.")

