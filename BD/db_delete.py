# BD/db_delete.py

import sqlite3
import os

def supprimer_employe(nom, prenom):
    """
    Supprime un employé de la base de données par nom et prénom.
    """
    # Chemin vers la base de données (optionnel : ajustez si nécessaire)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'employes.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employes WHERE nom = ? AND prenom = ?", (nom, prenom))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise ValueError(f"Aucun employé trouvé avec le nom '{nom}' et le prénom '{prenom}'.")
            
    except sqlite3.Error as e:
        raise Exception(f"Erreur base de données : {e}")
    finally:
        if conn:
            conn.close()