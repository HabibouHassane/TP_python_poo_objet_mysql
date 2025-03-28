from gestionnaire_contact import GestionnaireContact
from contact import Contact

class Main:
    def __init__(self):
        self.gestionnaire = GestionnaireContact()

    def afficher_menu(self):
        print("\n--- Gestionnaire de Contacts ---")
        print("1. Ajouter un nouveau contact")
        print("2. Consulter la liste des contacts")
        print("3. Rechercher un contact par nom")
        print("4. Modifier un contact")
        print("5. Supprimer un contact")
        print("6. Quitter")

    def ajouter_contact(self):
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ")
        telephone = input("Téléphone : ")
        contact = Contact(nom, prenom, email, telephone)
        self.gestionnaire.ajouter_contact(contact)

    def afficher_contacts(self):
        self.gestionnaire.afficher_contact()

    def rechercher_contact(self):
        nom = input("Nom du contact à rechercher : ")
        contact = self.gestionnaire.rechercher_contact(nom)
        if contact:
            print(contact)
        else:
            print("Contact introuvable.")

    def modifier_contact(self):
        nom = input("Nom du contact à modifier : ")
        self.gestionnaire.modifier_contact(nom)

    def supprimer_contact(self):
        telephone = input("Téléphone du contact à supprimer : ")
        self.gestionnaire.supprimer_contact(telephone)
        
    def quitter(self):
        """Ferme la connexion à la base de données et quitte l'application."""
        print("Fermeture de l'application...")
        self.gestionnaire.db.close_connection()  # Ferme la connexion à la base de données
        print("Connexion à la base de données fermée.")
        print("Au revoir !")
        exit(0)  # Quitte le programme proprement

    def run(self):
        """Lance le programme principal."""
        actions = {
            "1": self.ajouter_contact,
            "2": self.afficher_contacts,
            "3": self.rechercher_contact,
            "4": self.modifier_contact,
            "5": self.supprimer_contact,
            "6": self.quitter  # Associe "6" à la fonction quitter
        }

        while True:
            try:
                self.afficher_menu()
                choix = input("Votre choix : ")
                
                # Si le choix est valide, on exécute la fonction associée
                action = actions.get(choix)
                if action:
                    action()
                else:
                    print("Choix invalide, veuillez réessayer.")
                    
            except KeyboardInterrupt:
                print("\nOpération interrompue. Fermeture de l'application...")
                self.quitter()  # Appel à quitter en cas d'interruption manuelle

if __name__ == "__main__":
    print("Lancement de l'application...")
    app = Main()
    app.run()
