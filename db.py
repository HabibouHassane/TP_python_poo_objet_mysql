import mysql.connector

class Database:
    def __init__(self):
        """Initialise la connexion à MySQL au lancement de l'application."""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="contact"
            )
            if self.connection.is_connected():
                print("✅ Connexion réussie à MySQL")
                self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"❌ Erreur de connexion : {err}")
            self.connection = None
            self.cursor = None

    def fetch_data(self, query, values=None):
        """Exécute une requête SELECT et retourne les résultats."""
        if self.cursor:
            try:
                if values:
                    self.cursor.execute(query, values)
                else:
                    self.cursor.execute(query)
                return self.cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"⚠️ Erreur lors de l'exécution de la requête : {err}")
        return []

    def execute_query(self, query, values=None):
        """Exécute une requête INSERT, UPDATE ou DELETE."""
        if self.cursor:
            try:
                if values:
                    self.cursor.execute(query, values)
                else:
                    self.cursor.execute(query)
                self.connection.commit()
                print("✅ Requête exécutée avec succès")
            except mysql.connector.Error as err:
                print(f"⚠️ Erreur lors de l'exécution de la requête : {err}")

    def close_connection(self):
        """Ferme proprement la connexion MySQL."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔒 Connexion MySQL fermée.")

