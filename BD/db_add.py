import sqlite3

def ajouter_employe(nom, prenom, age, sexe, poste, salaire):
    conn = sqlite3.connect('employes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employes WHERE nom=? AND prenom=?', (nom, prenom))
    result = cursor.fetchone()
    if result:
        print(f"L'employé {nom} {prenom} existe déjà dans la base de données.")
    else:
        cursor.execute('''
            INSERT INTO employes (nom, prenom, age, sexe, poste, salaire)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nom, prenom, age, sexe, poste, salaire))
        conn.commit()
        print(f"Employé {nom} ajouté à la base de données.")
    conn.close()
