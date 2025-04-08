# Utiliser une image Python 3.13 comme image de base
FROM python:3.13-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances si requirements.txt existe
RUN pip install --no-cache-dir -r requirements.txt

# Commande pour exécuter l'application
CMD ["python", "main.py"]
