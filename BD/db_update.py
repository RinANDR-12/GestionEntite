import sqlite3

def modifier_employe(nom, prenom, nouvel_age=None, nouveau_sexe=None, nouveau_poste=None, nouveau_salaire=None):
    conn = sqlite3.connect('employes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employes WHERE nom=? AND prenom=?', (nom, prenom))
    result = cursor.fetchone()
    if not result:
        print(f"Aucun employé trouvé avec le nom {nom} et le prénom {prenom}.")
        conn.close()
        return
    # Prépare la requête de modification
    updates = []
    params = []
    if nouvel_age is not None:
        updates.append('age=?')
        params.append(nouvel_age)
    if nouveau_sexe is not None:
        updates.append('sexe=?')
        params.append(nouveau_sexe)
    if nouveau_poste is not None:
        updates.append('poste=?')
        params.append(nouveau_poste)
    if nouveau_salaire is not None:
        updates.append('salaire=?')
        params.append(nouveau_salaire)
    if updates:
        params.extend([nom, prenom])
        query = f"UPDATE employes SET {', '.join(updates)} WHERE nom=? AND prenom=?"
        cursor.execute(query, params)
        conn.commit()
        print(f"Employé {nom} {prenom} modifié dans la base de données.")
    else:
        print("Aucune donnée à modifier.")
    conn.close()
