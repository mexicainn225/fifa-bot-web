# database.py
# Stockage simple des utilisateurs en mémoire
utilisateurs = {} 

def ajouter_utilisateur(user_id, id_fifa):
    # On enregistre l'ID utilisateur et on met 'valide' à False par défaut
    utilisateurs[user_id] = {'id_fifa': id_fifa, 'valide': False}

def valider_utilisateur(user_id):
    # Passe le statut de l'utilisateur à True pour lui donner accès
    if user_id in utilisateurs:
        utilisateurs[user_id]['valide'] = True

def est_valide(user_id):
    # Vérifie si l'utilisateur est présent dans la liste et s'il est validé
    return utilisateurs.get(user_id, {}).get('valide', False)
