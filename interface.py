
import tkinter as tk
from tkinter import simpledialog
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'BD'))
from db_add import ajouter_employe
from db_show import afficher_employes
from db_update import modifier_employe
from db_delete import supprimer_employe

class GestionEntiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gestion des Employés')
        self.geometry('430x400')
        self.configure(bg='#f0f4f8')

        self.header = tk.Label(self, text='Gestion des Employés', font=('Arial', 20, 'bold'), bg='#4a90e2', fg='white', pady=10)
        self.header.pack(fill='x')

        self.frame = tk.Frame(self, bg='#f0f4f8')
        self.frame.pack(pady=20)

        self.message = tk.Label(self, text='', font=('Arial', 11), bg='#f0f4f8', fg='#333')
        self.message.pack(pady=5)

        self.create_buttons()

    def create_buttons(self):
        btn_style = {'font':('Arial', 12), 'width':20, 'height':2, 'bd':0, 'bg':'#e1eaff', 'activebackground':'#b3d1ff'}
        self.btn_ajouter = tk.Button(self.frame, text='Ajouter Employé', command=self.ajouter_employe, **btn_style)
        self.btn_ajouter.grid(row=0, column=0, padx=10, pady=10)
        self.btn_afficher = tk.Button(self.frame, text='Afficher Employés', command=self.afficher_employes, **btn_style)
        self.btn_afficher.grid(row=1, column=0, padx=10, pady=10)
        self.btn_modifier = tk.Button(self.frame, text='Modifier Employé', command=self.modifier_employe, **btn_style)
        self.btn_modifier.grid(row=2, column=0, padx=10, pady=10)
        self.btn_supprimer = tk.Button(self.frame, text='Supprimer Employé', command=self.supprimer_employe, **btn_style)
        self.btn_supprimer.grid(row=3, column=0, padx=10, pady=10)
        self.btn_quitter = tk.Button(self.frame, text='Quitter', command=self.quit, **btn_style)
        self.btn_quitter.grid(row=4, column=0, padx=10, pady=10)

        # Animation effet de survol
        for btn in [self.btn_ajouter, self.btn_afficher, self.btn_modifier, self.btn_supprimer, self.btn_quitter]:
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#4a90e2', fg='white'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#e1eaff', fg='black'))

    def set_message(self, msg, color='#333'):
        self.message.config(text=msg, fg=color)

    def ajouter_employe(self):
        nom = simpledialog.askstring('Nom', "Entrer le nom de l'employé:", parent=self)
        prenom = simpledialog.askstring('Prénom', 'Entrer le prénom:', parent=self)
        age = simpledialog.askinteger('Âge', 'Entrer l\'âge:', parent=self)
        sexe = simpledialog.askstring('Sexe', 'Entrer le sexe:', parent=self)
        poste = simpledialog.askstring('Poste', 'Entrer le poste:', parent=self)
        salaire = simpledialog.askinteger('Salaire', 'Entrer le salaire:', parent=self)
        if nom and prenom and age and sexe and poste and salaire:
            try:
                ajouter_employe(nom, prenom, age, sexe, poste, salaire)
                self.set_message('Employé ajouté avec succès !', '#228B22')
            except Exception as e:
                self.set_message(f'Erreur : {e}', 'red')
        else:
            self.set_message('Tous les champs sont obligatoires.', 'red')

    def afficher_employes(self):
        import sqlite3
        from tkinter import ttk
        # Supprime le tableau précédent s'il existe
        if hasattr(self, 'tree') and self.tree:
            self.tree.destroy()
        try:
            conn = sqlite3.connect('employes.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employes')
            rows = cursor.fetchall()
            conn.close()
            if not rows:
                self.set_message('Aucun employé enregistré.', 'orange')
                return
            columns = ("ID", "Nom", "Prénom", "Âge", "Sexe", "Poste", "Salaire")
            self.tree = ttk.Treeview(self, columns=columns, show='headings')
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=80)
            for row in rows:
                self.tree.insert('', 'end', values=row)
            self.tree.pack(pady=10)
            self.set_message(f'{len(rows)} employé(s) affiché(s).', '#333')
        except Exception as e:
            self.set_message(f'Erreur : {e}', 'red')

    def modifier_employe(self):
        nom = simpledialog.askstring('Nom', "Nom de l'employé à modifier:", parent=self)
        prenom = simpledialog.askstring('Prénom', 'Prénom de l\'employé à modifier:', parent=self)
        nouvel_age = simpledialog.askinteger('Âge', 'Nouveau âge (laisser vide si inchangé):', parent=self)
        nouveau_sexe = simpledialog.askstring('Sexe', 'Nouveau sexe (laisser vide si inchangé):', parent=self)
        nouveau_poste = simpledialog.askstring('Poste', 'Nouveau poste (laisser vide si inchangé):', parent=self)
        nouveau_salaire = simpledialog.askinteger('Salaire', 'Nouveau salaire (laisser vide si inchangé):', parent=self)
        if nom and prenom:
            try:
                modifier_employe(nom, prenom, nouvel_age, nouveau_sexe, nouveau_poste, nouveau_salaire)
                self.set_message('Employé modifié avec succès !', '#228B22')
            except Exception as e:
                self.set_message(f'Erreur : {e}', 'red')
        else:
            self.set_message('Nom et prénom obligatoires.', 'red')

    def supprimer_employe(self):
        nom = simpledialog.askstring('Nom', "Nom de l'employé à supprimer:", parent=self)
        prenom = simpledialog.askstring('Prénom', 'Prénom de l\'employé à supprimer:', parent=self)
        if nom and prenom:
            import tkinter.messagebox as mbox
            if mbox.askyesno('Confirmation', f'Supprimer {nom} {prenom} ?'):
                try:
                    supprimer_employe(nom, prenom)
                    self.set_message('Employé supprimé avec succès !', '#228B22')
                except Exception as e:
                    self.set_message(f'Erreur : {e}', 'red')
        else:
            self.set_message('Nom et prénom obligatoires.', 'red')

if __name__ == '__main__':
    app = GestionEntiteApp()
    app.mainloop()
    # ...existing code...
