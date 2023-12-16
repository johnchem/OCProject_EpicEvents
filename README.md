# Installation de postgreSQL
- télécharger le gestionnaire de base de donnée PostgreSQL depuis https://www.postgresql.org/download/
- Lors de l'installation, il sera demander de définir un mot de passe pour l'utilisateur **postgres**. Bien noté le mot de passe car il sera nécéssaire dans la configuration de l'application

# Récupération du repo
- Ouvrir la console et se déplacer dans le dossier source
- exécuter la commande `git clone https://github.com/johnchem/OCProject_EpicEvents.git`
- se déplacer dans le dossier `cd OCProject_EpicEvents`

# initialisation de l'environnement virtuel
- dans le dossier `OCProject_EpicEvents`
- crée l'environnement virtuel avec la commande `python -m venv .venv`
- démarrer l'environnement virtuel `.venv\Scripts\activate`

# installation des dépendances
- mettre à jour pip
    ```
    python3 -m pip install --upgrade pip
    python3 -m pip --version
    ```
- installer les libraries nécéssaire avec la commande `python3 -m pip install -r requirements.txt`

# configuration de l'application
- créer une copie du fichier `OCProject_EpicEvents/epicevent/.env.exemple` en le nommant `.env`
- remplir les informations demander dans le fichier 

## gestion de psql (PSQL)
- l'adresse pour la console pqsl est sous `%PATH%\PostgreSQL\15\bin\psql.exe` avec `%PATH%` étant le dossier d'installation de Postgres

## Adresse du serveur (SERVER; PORT)
- Par défaut, le serveur postgre est monté sur **localhost** sur le port **5433**
- Adapter ces valeurs selon votre configuration

## Identification d'accés au serveur (ADMIN_LOGIN; PGPASSWORD)
- lors de la configuration du serveur, un compte admin et un mot de passe sera demandé.
- les informations de connection doivent être introduite dans ces champs

## Indentification de gestion de la base de données (DATABASE_NAME; DATABASE_LOGIN; DATABASE_PWD)
- définir un nom pour la base de données
- définir l'identifiant et le mot de passe de connection pour le compte administrateur de la base de donnnées
**Note:** ce compte n'est administrateur dans l'application, il est utilisé pour gérer les transactions entre la base de donnée et l'application

## Définition de la durée d'expiration des token JWT (EXPIRATION_TIME_TOKEN)
- introduire la durée **en s** avant l'expiration et le renouvellement du token d'authentification

## configuration de Sentry (SENTRY_KEY)
- dans l'application Sentry, cliquer sur l'option **Create Project**
- Choisissez un nouveau projet **Python**
- définissez vos préférences pour la fréquence d'alerte
- choisissz le nom du projet et l'équipe responsable puis cliquez sur **Create Project**
- Sentry va fournir une clef. Celle-ci doit être collé dans le champs du .env sans les guillemets  
