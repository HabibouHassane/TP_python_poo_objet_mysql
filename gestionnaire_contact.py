import os
from contact import Contact
from utils import saisir_champ

from db import Database



class GestionnaireContact:
    def __init__(self):
        self.db = Database()  # Connexion à la base de données
        self.liste_contact = self.charger_contacts()

    def charger_contacts(self):
        """Charge les contacts depuis la base de données."""
        query = "SELECT nom, prenom, email, telephone FROM contact"
        contacts = self.db.fetch_data(query)
        return [Contact(nom, prenom, email, telephone) for nom, prenom, email, telephone in contacts]

    def sauvegarder_contact(self, contact):
        """Sauvegarde ou met à jour un contact dans la base de données."""
        if not contact:
            print("⚠️ Aucun contact à sauvegarder.")
            return

        query = """
            INSERT INTO contact (nom, prenom, email, telephone)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            nom = VALUES(nom), prenom = VALUES(prenom), telephone = VALUES(telephone)
        """
        values = (contact.get_nom(), contact.get_prenom(), contact.get_email(), contact.get_telephone())
        self.db.execute_query(query, values)

    def ajouter_contact(self, contact):
        """Ajoute un contact après vérification d'unicité."""
        if any(c.get_telephone() == contact.get_telephone() or c.get_email() == contact.get_email() for c in self.liste_contact):
            print("Le contact existe déjà !")
            return

        self.sauvegarder_contact(contact)
        print("Contact ajouté avec succès !")
        self.liste_contact.append(contact)  # Met à jour la liste locale

    def afficher_contact(self):
        """Affiche tous les contacts."""
        if self.liste_contact:
            for contact in self.liste_contact:
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
        """Modifie les informations d'un contact."""
        contact = self.rechercher_contact(nom)
        if contact:
            fields = ['nom', 'prenom', 'email', 'télephone']
            for field in fields:
                value = input(f"{field} (laisser vide pour ne pas changer) : ")
                if value:
                    getattr(contact, f'set_{field}')(value)
            self.sauvegarder_contact(contact)
            print("Contact modifié avec succès.")
        else:
            print("Contact introuvable.")

    def supprimer_contact(self, telephone):
        """Supprime un contact de la base de données et de la liste locale."""
        
        # Vérifier si le contact existe dans la base de données
        query = f"SELECT 1 FROM contact WHERE telephone = '{telephone}'"
        contact = self.db.fetch_data(query)  # On passe la requête pour récupérer les résultats

        if not contact:
            print(f"Aucun contact trouvé avec le téléphone {telephone}.")
            return

        # Si le contact existe, on le supprime de la base de données
        delete_query = f"DELETE FROM contact WHERE telephone = '{telephone}'"
        try:
            self.db.execute_query(delete_query)  # Exécuter la requête de suppression
            print(f"Le contact avec le téléphone {telephone} a été supprimé de la base de données.")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du contact : {e}")
            return
        
        # Supprimer également le contact de la liste locale
        self.liste_contact = [contact for contact in self.liste_contact if contact.get_telephone() != telephone]
        print(f"Le contact avec le téléphone {telephone} a été supprimé de la liste locale.")
