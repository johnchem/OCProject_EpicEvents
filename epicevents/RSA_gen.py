from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import os


def generate_RSA_pair():
    # Générer une paire de clés RSA
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    # Sérialiser la clé privée au format PEM
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Récupérer la clé publique
    public_key = private_key.public_key()

    # Sérialiser la clé publique au format PEM
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Convertir les clés en chaînes pour les variables d'environnement
    private_key_str = pem_private.decode("utf-8")
    public_key_str = pem_public.decode("utf-8")

    # Définir les variables d'environnement
    os.environ["PRIVATE_KEY"] = private_key_str
    os.environ["PUBLIC_KEY"] = public_key_str
