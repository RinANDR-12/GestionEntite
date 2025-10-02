import sqlite3

def supprimer_employe(nom, prenom):
    conn = sqlite3.connect('employes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employes WHERE nom=? AND prenom=?', (nom, prenom))
    result = cursor.fetchone()
    if result:
        cursor.execute('DELETE FROM employes WHERE nom=? AND prenom=?', (nom, prenom))
        conn.commit()
        print(f"Employé {nom} {prenom} supprimé de la base de données.")
    else:
        print(f"Aucun employé trouvé avec le nom {nom} et le prénom {prenom}.")
    # Afficher tous les employés restants
    cursor.execute('SELECT * FROM employes')
    rows = cursor.fetchall()
    if not rows:
        print("Aucun employé enregistré.")
    else:
        print("Liste des employés dans la base de données :")
        for row in rows:
            print(f"ID: {row[0]}, Nom: {row[1]}, Prénom: {row[2]}, Âge: {row[3]}, Sexe: {row[4]}, Poste: {row[5]}, Salaire: {row[6]}")
    print("\n")
    print("--------------------------------------------------")
    print("Base de données mise à jour : ")
    conn.close()
