import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        """Initialise la connexion à MySQL et la table contacts."""
        try:
            self.connection = mysql.connector.connect(
                host="mysql_db",  # nom du service docker-compose
                user="vde",
                password="vde",
                database="contact"
            )

            if self.connection.is_connected():
                print("✅ Connexion réussie à MySQL")
                self.cursor = self.connection.cursor()
                self._init_table()
            else:
                print("❌ La connexion à MySQL a échoué.")
                self.cursor = None

        except Error as err:
            print(f"❌ Erreur de connexion à MySQL : {err}")
            self.connection = None
            self.cursor = None

    def _init_table(self):
        """Crée la table 'contacts' si elle n'existe pas."""
        try:
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'contact'
                AND table_name = 'contacts';
            """)
            exists = self.cursor.fetchone()[0]
            if exists == 0:
                print("🛠️ Table 'contacts' non trouvée. Création en cours...")
                self.cursor.execute("""
                    CREATE TABLE contacts (
                        nom VARCHAR(100),
                        prenom VARCHAR(100),
                        email VARCHAR(100),
                        telephone VARCHAR(100)
                    );
                """)
                self.connection.commit()
                print("✅ Table 'contacts' créée avec succès.")
            else:
                print("✅ Table 'contacts' déjà existante.")
        except Error as err:
            print(f"⚠️ Erreur lors de la vérification de la table : {err}")

    def fetch_data(self, query, values=None):
        """Exécute une requête SELECT et retourne les résultats."""
        if self.cursor:
            try:
                if values:
                    self.cursor.execute(query, values)
                else:
                    self.cursor.execute(query)
                return self.cursor.fetchall()
            except Error as err:
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
            except Error as err:
                print(f"⚠️ Erreur lors de l'exécution de la requête : {err}")

    def close_connection(self):
        """Ferme proprement la connexion MySQL."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔒 Connexion MySQL fermée.")
