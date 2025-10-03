import tkinter as tk
from tkinter import ttk, messagebox, font
import sys, os
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), 'BD'))
from db_add import ajouter_employe
from db_show import afficher_employes
from db_update import modifier_employe_par_id  # 🔸 IMPORT CORRIGÉ
from db_delete import supprimer_employe


class AjoutEmployeForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajouter un Employé")
        self.result = None
        self.parent = parent

        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.configure(bg="#252526")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width, height = 420, 380
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

        label_font = font.Font(family="Segoe UI", size=11)
        entry_font = font.Font(family="Segoe UI", size=11)
        button_font = font.Font(family="Segoe UI", size=10, weight="bold")

        tk.Label(
            self,
            text="📝 Nouvel Employé",
            font=("Segoe UI", 14, "bold"),
            bg="#252526",
            fg="#4dabf7"
        ).pack(pady=(15, 20))

        form_frame = tk.Frame(self, bg="#252526")
        form_frame.pack(padx=20, pady=(0, 15), fill="x")

        self.entries = {}
        fields = [
            ("Nom", "nom"),
            ("Prénom", "prenom"),
            ("Âge (16-65)", "age"),
            ("Sexe (M/F)", "sexe"),
            ("Poste", "poste"),
            ("Salaire (≥ 0)", "salaire")
        ]

        for i, (label_text, key) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label_text + " :",
                font=label_font,
                bg="#252526",
                fg="#e0e0e0",
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=6)

            entry = tk.Entry(
                form_frame,
                font=entry_font,
                relief="flat",
                bg="#1e1e1e",
                fg="#e0e0e0",
                insertbackground="#4dabf7",
                highlightthickness=1,
                highlightbackground="#3c3c40",
                highlightcolor="#4dabf7"
            )
            entry.grid(row=i, column=1, padx=(10, 0), pady=6, sticky="ew")
            self.entries[key] = entry

        form_frame.grid_columnconfigure(1, weight=1)
        self.entries["nom"].focus_set()

        btn_frame = tk.Frame(self, bg="#252526")
        btn_frame.pack(pady=(0, 15))

        tk.Button(
            btn_frame,
            text="Annuler",
            command=self.cancel,
            font=button_font,
            bg="#5a5a5a",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=6,
            activebackground="#6e6e6e",
            activeforeground="white"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ajouter",
            command=self.submit,
            font=button_font,
            bg="#4dabf7",
            fg="#121212",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=6,
            activebackground="#6ecff6",
            activeforeground="#121212"
        ).pack(side="left", padx=5)

        self.bind("<Return>", lambda e: self.submit())
        self.bind("<Escape>", lambda e: self.cancel())

    def validate(self):
        data = {}
        errors = []

        nom = self.entries["nom"].get().strip()
        if not nom or len(nom) < 2:
            errors.append("Nom trop court (min. 2 caractères)")
        else:
            data["nom"] = nom

        prenom = self.entries["prenom"].get().strip()
        if not prenom or len(prenom) < 2:
            errors.append("Prénom trop court (min. 2 caractères)")
        else:
            data["prenom"] = prenom

        try:
            age = int(self.entries["age"].get().strip())
            if not (16 <= age <= 65):
                errors.append("Âge invalide (doit être entre 16 et 65)")
            else:
                data["age"] = age
        except ValueError:
            errors.append("Âge invalide (doit être un nombre entier)")

        sexe = self.entries["sexe"].get().strip().upper()
        if sexe not in ["M", "F"]:
            errors.append("Sexe invalide (M ou F)")
        else:
            data["sexe"] = sexe

        poste = self.entries["poste"].get().strip()
        if not poste or len(poste) < 2:
            errors.append("Poste trop court (min. 2 caractères)")
        else:
            data["poste"] = poste

        try:
            salaire = int(self.entries["salaire"].get().strip())
            if salaire < 0:
                errors.append("Salaire invalide (doit être ≥ 0)")
            else:
                data["salaire"] = salaire
        except ValueError:
            errors.append("Salaire invalide (doit être un nombre entier)")

        return data if not errors else errors

    def submit(self):
        result = self.validate()
        if isinstance(result, list):
            messagebox.showwarning(
                "Champs invalides",
                "Veuillez corriger les erreurs suivantes :\n• " + "\n• ".join(result),
                parent=self
            )
            return

        self.result = result
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()


class ModifierEmployeForm(tk.Toplevel):
    def __init__(self, parent, employe_data):
        super().__init__(parent)
        self.title("Modifier un Employé")
        self.result = None
        self.parent = parent
        self.employe_data = employe_data  # (id, nom, prenom, age, sexe, poste, salaire)

        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.configure(bg="#252526")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width, height = 420, 380
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

        label_font = font.Font(family="Segoe UI", size=11)
        entry_font = font.Font(family="Segoe UI", size=11)
        button_font = font.Font(family="Segoe UI", size=10, weight="bold")

        tk.Label(
            self,
            text="✏️ Modifier Employé",
            font=("Segoe UI", 14, "bold"),
            bg="#252526",
            fg="#4dabf7"
        ).pack(pady=(15, 20))

        form_frame = tk.Frame(self, bg="#252526")
        form_frame.pack(padx=20, pady=(0, 15), fill="x")

        self.entries = {}
        fields = [
            ("Nom", "nom", employe_data[1]),
            ("Prénom", "prenom", employe_data[2]),
            ("Âge (16-65)", "age", str(employe_data[3])),
            ("Sexe (M/F)", "sexe", employe_data[4]),
            ("Poste", "poste", employe_data[5]),
            ("Salaire (≥ 0)", "salaire", str(employe_data[6]))
        ]

        for i, (label_text, key, value) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label_text + " :",
                font=label_font,
                bg="#252526",
                fg="#e0e0e0",
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=6)

            entry = tk.Entry(
                form_frame,
                font=entry_font,
                relief="flat",
                bg="#1e1e1e",
                fg="#e0e0e0",
                insertbackground="#4dabf7",
                highlightthickness=1,
                highlightbackground="#3c3c40",
                highlightcolor="#4dabf7"
            )
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=(10, 0), pady=6, sticky="ew")
            self.entries[key] = entry

        form_frame.grid_columnconfigure(1, weight=1)
        self.entries["nom"].focus_set()

        btn_frame = tk.Frame(self, bg="#252526")
        btn_frame.pack(pady=(0, 15))

        tk.Button(
            btn_frame,
            text="Annuler",
            command=self.cancel,
            font=button_font,
            bg="#5a5a5a",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=6,
            activebackground="#6e6e6e",
            activeforeground="white"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Modifier",
            command=self.submit,
            font=button_font,
            bg="#4dabf7",
            fg="#121212",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=6,
            activebackground="#6ecff6",
            activeforeground="#121212"
        ).pack(side="left", padx=5)

        self.bind("<Return>", lambda e: self.submit())
        self.bind("<Escape>", lambda e: self.cancel())

    def validate(self):
        data = {}
        errors = []

        nom = self.entries["nom"].get().strip()
        if not nom or len(nom) < 2:
            errors.append("Nom trop court (min. 2 caractères)")
        else:
            data["nom"] = nom

        prenom = self.entries["prenom"].get().strip()
        if not prenom or len(prenom) < 2:
            errors.append("Prénom trop court (min. 2 caractères)")
        else:
            data["prenom"] = prenom

        try:
            age = int(self.entries["age"].get().strip())
            if not (16 <= age <= 65):
                errors.append("Âge invalide (doit être entre 16 et 65)")
            else:
                data["age"] = age
        except ValueError:
            errors.append("Âge invalide (doit être un nombre entier)")

        sexe = self.entries["sexe"].get().strip().upper()
        if sexe not in ["M", "F"]:
            errors.append("Sexe invalide (M ou F)")
        else:
            data["sexe"] = sexe

        poste = self.entries["poste"].get().strip()
        if not poste or len(poste) < 2:
            errors.append("Poste trop court (min. 2 caractères)")
        else:
            data["poste"] = poste

        try:
            salaire = int(self.entries["salaire"].get().strip())
            if salaire < 0:
                errors.append("Salaire invalide (doit être ≥ 0)")
            else:
                data["salaire"] = salaire
        except ValueError:
            errors.append("Salaire invalide (doit être un nombre entier)")

        return data if not errors else errors

    def submit(self):
        result = self.validate()
        if isinstance(result, list):
            messagebox.showwarning(
                "Champs invalides",
                "Veuillez corriger les erreurs suivantes :\n• " + "\n• ".join(result),
                parent=self
            )
            return

        self.result = result
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()


class GestionEntiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gestion des Employés')
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = min(900, int(screen_width * 0.7))
        window_height = min(700, int(screen_height * 0.8))
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        self.configure(bg="#1e1e1e")
        self.minsize(600, 500)
        self.resizable(True, True)

        self.setup_fonts()

        self.left_panel = tk.Frame(self, bg="#252526", width=180)
        self.left_panel.pack(side="left", fill="y")
        self.left_panel.pack_propagate(False)

        self.header = tk.Label(
            self.left_panel,
            text='Gestion\n des Employés',
            font=self.title_font,
            bg='#252526',
            fg='#e0e0e0',
            pady=25,
            padx=10,
            justify="center"
        )
        self.header.pack(fill="x")

        separator = tk.Frame(self.left_panel, bg="#3c3c40", height=1)
        separator.pack(fill="x", padx=10, pady=(0, 20))

        self.create_sidebar_buttons()

        self.content_frame = tk.Frame(self, bg="#1e1e1e")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.content_frame.grid_rowconfigure(2, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.message = tk.Label(
            self.content_frame,
            text='',
            font=self.base_font,
            bg='#1e1e1e',
            fg='#a0a0a0',
            wraplength=600
        )
        self.message.grid(row=0, column=0, pady=(0, 5), sticky="ew")

        self.create_search_bar()

        self.tree_frame = tk.Frame(self.content_frame, bg="#1e1e1e")
        self.tree_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = None
        self.bind('<Configure>', self.on_window_resize)

        self.after(100, self.afficher_employes)

    def setup_fonts(self):
        default_font = font.nametofont("TkDefaultFont")
        base_size = max(9, min(12, default_font['size']))
        title_size = max(16, min(24, int(base_size * 1.7)))
        self.base_font = font.Font(family="Segoe UI", size=base_size)
        self.button_font = font.Font(family="Segoe UI", size=base_size, weight="bold")
        self.title_font = font.Font(family="Segoe UI", size=title_size, weight="bold")

    def on_window_resize(self, event=None):
        if event and event.widget == self:
            width = self.content_frame.winfo_width()
            self.message.config(wraplength=max(400, width - 40))
            if self.tree:
                self.after(100, self.update_treeview_columns)

    def create_sidebar_buttons(self):
        buttons_info = [
            ("👤 Ajouter", self.ajouter_employe),
            ("🚪 Quitter", self.quit)
        ]

        for text, cmd in buttons_info:
            btn = tk.Button(
                self.left_panel,
                text=text,
                command=cmd,
                font=("Segoe UI", 11, "bold"),
                bg="#3e3e42",
                fg="#e0e0e0",
                relief='flat',
                cursor='hand2',
                activebackground="#4a4a4f",
                activeforeground="#ffffff",
                padx=15,
                pady=12,
                anchor="w"
            )
            btn.pack(pady=8, padx=15, fill="x")
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg="#4a4a4f"))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg="#3e3e42"))

    def create_search_bar(self):
        search_frame = tk.Frame(self.content_frame, bg="#1e1e1e")
        search_frame.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)

        tk.Label(
            search_frame,
            text="🔍 Rechercher :",
            font=self.base_font,
            bg="#1e1e1e",
            fg="#a0a0a0"
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.base_font,
            relief="flat",
            bg="#252526",
            fg="#e0e0e0",
            insertbackground="#4dabf7",
            highlightthickness=1,
            highlightbackground="#3c3c40",
            highlightcolor="#4dabf7"
        )
        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew", ipady=4)

        reset_btn = tk.Button(
            search_frame,
            text="Réinitialiser",
            command=self.clear_search,
            font=("Segoe UI", 9, "bold"),
            bg="#5a5a5a",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#6e6e6e",
            activeforeground="white",
            padx=10,
            pady=2
        )
        reset_btn.grid(row=0, column=2)

        self.search_var.trace_add("write", self.on_search_change)

    # =============== MENU CONTEXTUEL ===============
    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✏️ Modifier", command=self.context_modifier)
        self.context_menu.add_command(label="🗑️ Supprimer", command=self.context_supprimer)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Annuler", command=self.context_menu.unpost)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Button-2>", self.show_context_menu)

    def show_context_menu(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            if item:
                self.tree.selection_set(item)
                try:
                    self.context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    self.context_menu.grab_release()

    def context_modifier(self):
        item = self.tree.focus()
        if not item:
            self.set_message("⚠️ Veuillez sélectionner une ligne.", "#ffd43b")
            return
        
        values = self.tree.item(item, "values")
        if not values or len(values) < 7:
            self.set_message("❌ Données employé incomplètes.", "#ff6b6b")
            return

        try:
            employe_id = int(values[0])
            nom = str(values[1]).strip()
            prenom = str(values[2]).strip()
            age = int(values[3])
            sexe = str(values[4]).strip().upper()
            poste = str(values[5]).strip()
            salaire = int(values[6])
            
            if not nom or not prenom or age < 0 or salaire < 0 or sexe not in ["M", "F"]:
                self.set_message("❌ Données invalides.", "#ff6b6b")
                return

            employe_data = (employe_id, nom, prenom, age, sexe, poste, salaire)
            self.modifier_employe_direct(employe_data)
            
        except Exception as e:
            self.set_message("❌ Erreur : données employé invalides.", "#ff6b6b")

    def context_supprimer(self):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, "values")
        if values and len(values) >= 3:
            employe_id, nom, prenom = values[0], values[1], values[2]
            self.supprimer_employe_direct(employe_id, nom, prenom)

    # =============== ACTIONS ===============
    def modifier_employe_direct(self, employe_data):
        """employe_data = (id, nom, prenom, age, sexe, poste, salaire)"""
        form = ModifierEmployeForm(self, employe_data)
        self.wait_window(form)
        
        if form.result:
            data = form.result
            try:
                # 🔸 UTILISATION DE L'ID POUR LA MODIFICATION
                modifier_employe_par_id(
                    employe_id=employe_data[0],
                    nouvel_age=data["age"],
                    nouveau_sexe=data["sexe"],
                    nouveau_poste=data["poste"],
                    nouveau_salaire=data["salaire"]
                )
                self.set_message('✅ Employé modifié avec succès !', '#69db7c')
                self.afficher_employes()
            except Exception as e:
                self.set_message(f'❌ Erreur : {e}', '#ff6b6b')

    def supprimer_employe_direct(self, employe_id, nom, prenom):
        if messagebox.askyesno('Confirmation', f'Supprimer {nom} {prenom} ?', parent=self):
            try:
                supprimer_employe(nom, prenom)
                self.set_message('✅ Employé supprimé avec succès !', '#69db7c')
                self.afficher_employes()
            except Exception as e:
                self.set_message(f'❌ Erreur : {e}', '#ff6b6b')

    # =============== TABLEAU ===============
    def on_search_change(self, *args):
        if hasattr(self, '_search_cache') and self._search_cache:
            self.filter_employees(self.search_var.get())

    def clear_search(self):
        self.search_var.set("")
        if hasattr(self, '_search_cache') and self._search_cache:
            self.display_employees_from_cache()

    def cache_employees(self, rows):
        self._search_cache = rows

    def display_employees_from_cache(self):
        self.clear_treeview()
        self.display_employees_in_tree(self._search_cache)

    def filter_employees(self, query):
        if not query.strip():
            self.display_employees_from_cache()
            return

        query = query.lower()
        filtered = [
            row for row in self._search_cache
            if query in row[1].lower() or query in row[2].lower()
        ]
        self.clear_treeview()
        self.display_employees_in_tree(filtered)
        self.set_message(f'🔍 {len(filtered)} résultat(s) pour "{query}".', '#6ecff6')

    def display_employees_in_tree(self, rows):
        if not rows:
            self.set_message('ℹ️ Aucun employé trouvé.', '#f39c12')
            return

        columns = ("ID", "Nom", "Prénom", "Âge", "Sexe", "Poste", "Salaire")
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show='headings',
            height=min(18, len(rows))
        )

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#2d2d2d",
            foreground="#e0e0e0",
            relief="flat"
        )
        style.configure("Treeview",
            background="#252526",
            foreground="#e0e0e0",
            rowheight=28,
            fieldbackground="#252526",
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.map("Treeview",
            background=[('selected', '#4dabf7')],
            foreground=[('selected', '#121212')]
        )

        col_widths = [40, 100, 100, 50, 50, 120, 80]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')

        for row in rows:
            self.tree.insert('', 'end', values=row)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.create_context_menu()

    def set_message(self, msg, color='#a0a0a0'):
        self.message.config(text=msg, fg=color)

    def clear_treeview(self):
        if self.tree:
            self.tree.destroy()
            self.tree = None

    def update_treeview_columns(self):
        if not self.tree or not self.tree.winfo_ismapped():
            return
        total_width = self.tree_frame.winfo_width() - 20
        if total_width < 100:
            return
        ratios = [0.08, 0.17, 0.17, 0.10, 0.10, 0.23, 0.15]
        columns = ("ID", "Nom", "Prénom", "Âge", "Sexe", "Poste", "Salaire")
        for i, col in enumerate(columns):
            width = max(40, int(total_width * ratios[i]))
            self.tree.column(col, width=width, anchor='center')

    def afficher_employes(self):
        try:
            conn = sqlite3.connect('employes.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employes')
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                self.set_message('ℹ️ Aucun employé enregistré.', '#f39c12')
                self.clear_treeview()
                if hasattr(self, '_search_cache'):
                    del self._search_cache
                return

            self.cache_employees(rows)
            self.clear_treeview()
            self.display_employees_in_tree(rows)
            self.set_message(f'✅ {len(rows)} employé(s) affiché(s).', '#69db7c')

        except Exception as e:
            self.set_message(f'❌ Erreur : {e}', '#ff6b6b')

    def ajouter_employe(self):
        form = AjoutEmployeForm(self)
        self.wait_window(form)
        
        if form.result:
            data = form.result
            try:
                ajouter_employe(
                    data["nom"],
                    data["prenom"],
                    data["age"],
                    data["sexe"],
                    data["poste"],
                    data["salaire"]
                )
                self.set_message('✅ Employé ajouté avec succès !', '#69db7c')
                self.afficher_employes()
            except sqlite3.IntegrityError:
                self.set_message('❌ Cet employé existe déjà.', '#ff6b6b')
            except Exception as e:
                self.set_message(f'❌ Erreur : {e}', '#ff6b6b')


if __name__ == '__main__':
    app = GestionEntiteApp()
    app.mainloop(