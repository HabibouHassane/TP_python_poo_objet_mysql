import os
from contact import Contact
from utils import saisir_champ
from db import Database

class GestionnaireContact:
    def __init__(self):
        self.db = Database()
        self.liste_contact = self.charger_contacts()

    def charger_contacts(self):
        """Charge les contacts depuis la base de données."""
        query = "SELECT nom, prenom, email, telephone FROM contact"
        contacts = self.db.fetch_data(query)
        return [Contact(nom, prenom, email, telephone) for nom, prenom, email, telephone in contacts]

    def ajouter_contact(self, contact):
        """Ajoute un contact après vérification d'unicité."""
        if any(c.get_telephone() == contact.get_telephone() or c.get_email() == contact.get_email() for c in self.liste_contact):
            print("Le contact existe déjà !")
            return

        query = """
            INSERT INTO contact (nom, prenom, email, telephone)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            nom = VALUES(nom), prenom = VALUES(prenom), telephone = VALUES(telephone)
        """
        values = (contact.get_nom(), contact.get_prenom(), contact.get_email(), contact.get_telephone())
        self.db.execute_query(query, values)
        print("Contact ajouté avec succès !")
        self.liste_contact.append(contact)

    def afficher_contact(self):
        """Affiche tous les contacts."""
        if self.liste_contact:
            for cont in self.liste_contact:
                print(f"Nom : {cont.get_nom()} Prénom : {cont.get_prenom()} Téléphone : {cont.get_telephone()} Email : {cont.get_email()}")
        else:
            print("Aucun contact enregistré.")

    def rechercher_contact(self, nom):
        """Recherche un contact par son nom."""
        for contact in self.liste_contact:
            if contact.get_nom().lower() == nom.lower():
                return contact
        return None

    def modifier_contact(self, nom):
        """Modifie les informations d'un contact en utilisant UPDATE."""
        contact = self.rechercher_contact(nom)
        if contact:
            updates = {}
            fields = {'nom': 'nom', 'prenom': 'prenom', 'email': 'email', 'télephone': 'telephone'}
            for field, db_field in fields.items():
                value = input(f"{field} (laisser vide pour ne pas changer) : ")
                if value:
                    updates[db_field] = value
                    getattr(contact, f'set_{field}')(value)
            
            if updates:
                set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
                query = f"""
                    UPDATE contact
                    SET {set_clause}
                    WHERE email = %s OR telephone = %s
                """
                values = list(updates.values()) + [contact.get_email(), contact.get_telephone()]
                self.db.execute_query(query, values)
                print("Contact modifié avec succès.")
                
                # Mettre à jour la liste locale
                self.liste_contact = self.charger_contacts()
            else:
                print("Aucune modification apportée.")
        else:
            print("Contact introuvable.")

    def supprimer_contact(self, telephone):
        """Supprime un contact de la base de données et de la liste locale."""
        query = "SELECT 1 FROM contact WHERE telephone = %s"
        contact = self.db.fetch_data(query, (telephone,))

        if not contact:
            print(f"Aucun contact trouvé avec le téléphone {telephone}.")
            return

        delete_query = "DELETE FROM contact WHERE telephone = %s"
        try:
            self.db.execute_query(delete_query, (telephone,))
            print(f"Le contact avec le téléphone {telephone} a été supprimé de la base de données.")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du contact : {e}")
            return

        self.liste_contact = [c for c in self.liste_contact if c.get_telephone() != telephone]
        print(f"Le contact avec le téléphone {telephone} a été supprimé de la liste locale.")
