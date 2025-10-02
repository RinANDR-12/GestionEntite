import sqlite3

def afficher_employes():
    conn = sqlite3.connect('employes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employes')
    rows = cursor.fetchall()

    print("\n")
    print("--------------------------------------------------") 
    print("Liste des employés dans la base de données :")
    if not rows:
        print("Aucun employé enregistré.")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Nom: {row[1]}, Prénom: {row[2]}, Âge: {row[3]}, Sexe: {row[4]} , Poste: {row[5]}, Salaire: {row[6]} Ar ")
    conn.close()
