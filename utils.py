def saisir_champ(nom_champ, valeur_actuelle=""):
        """
        Demande à l'utilisateur de saisir une nouvelle valeur pour un champ.
        Si l'utilisateur laisse vide, retourne la valeur actuelle.
        """
        saisie = input(f"Nouveau {nom_champ} ({valeur_actuelle}): ").strip()
        return saisie if saisie else valeur_actuelle