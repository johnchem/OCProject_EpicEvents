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