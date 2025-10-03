import sqlite3
import os

def modifier_employe(employe_id, nouvel_age=None, nouveau_sexe=None, nouveau_poste=None, nouveau_salaire=None):
    """
    Modifie un employé par son ID (méthode fiable)
    Les paramètres à None ne seront pas modifiés.
    """
    # Chemin vers la base de données (doit être au même niveau que le dossier BD)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'employes.db')
    
    # Vérifier que la base existe
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Base de données introuvable : {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Construire la requête dynamiquement
    updates = []
    params = []
    
    if nouvel_age is not None:
        updates.append("age = ?")
        params.append(nouvel_age)
    if nouveau_sexe is not None:
        updates.append("sexe = ?")
        params.append(nouveau_sexe)
    if nouveau_poste is not None:
        updates.append("poste = ?")
        params.append(nouveau_poste)
    if nouveau_salaire is not None:
        updates.append("salaire = ?")
        params.append(nouveau_salaire)
    
    if not updates:
        conn.close()
        return  # Rien à modifier
    
    # Ajouter l'ID à la fin des paramètres
    params.append(employe_id)
    query = f"UPDATE employes SET {', '.join(updates)} WHERE id = ?"
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()