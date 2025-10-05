import tkinter as tk
from tkinter import ttk, messagebox, font
import sys, os
import sqlite3
import calendar
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'BD'))
from db_add import ajouter_employe
from db_show import afficher_employes
from db_update import modifier_employe
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
        self.employe_data = employe_data

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
        self.minsize(800, 600)
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
        self.content_frame.grid_rowconfigure(3, weight=1)
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

        # === Barre de recherche : créée dès le départ ===
        self.search_frame = tk.Frame(self.content_frame, bg="#1e1e1e")
        self.search_frame.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        self.search_frame.grid_columnconfigure(1, weight=1)

        tk.Label(
            self.search_frame,
            text="🔍 Rechercher :",
            font=self.base_font,
            bg="#1e1e1e",
            fg="#a0a0a0"
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.search_frame,
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
            self.search_frame,
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

        self.button_frame = tk.Frame(self.content_frame, bg="#1e1e1e")
        self.button_frame.grid(row=2, column=0, pady=(10, 0), sticky="ew")
        
        self.ajout_btn = tk.Button(
            self.button_frame,
            text="👤 Ajouter",
            command=self.ajouter_employe,
            font=("Segoe UI", 10, "bold"),
            bg="#4dabf7",
            fg="white",
            relief='flat',
            cursor='hand2',
            activebackground="#6ecff6",
            activeforeground="white",
            padx=10,
            pady=5,
            bd=0,
            highlightthickness=0
        )
        self.ajout_btn.pack(side="right", padx=5, pady=5)
        self.ajout_btn.bind('<Enter>', lambda e, b=self.ajout_btn: b.config(bg="#6ecff6"))
        self.ajout_btn.bind('<Leave>', lambda e, b=self.ajout_btn: b.config(bg="#4dabf7"))

        self.current_view = "tableau"

        self.tree_frame = tk.Frame(self.content_frame, bg="#1e1e1e")
        self.tree_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 0))
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = None
        self.bind('<Configure>', self.on_window_resize)

        # Vérification base de données
        try:
            sqlite3.connect('employes.db').close()
        except sqlite3.Error:
            messagebox.showerror("Erreur", "Impossible de se connecter à la base de données")
            sys.exit(1)

        if not os.path.exists('employes.db'):
            messagebox.showerror("Erreur", "Base de données introuvable")
            sys.exit(1)

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
            ("📅 Planning", self.afficher_planning),
            ("📊 Tableau", self.afficher_employes)
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
        if not values:
            self.set_message("❌ Données employé incomplètes.", "#ff6b6b")
            return

        try:
            employe_data = (
                int(values[0]),
                str(values[1]),
                str(values[2]),
                int(values[3]),
                str(values[4]).upper(),
                str(values[5]),
                float(values[6])
            )
            self.modifier_employe_direct(employe_data)
            
        except (ValueError, IndexError) as e:
            self.set_message(f"❌ Erreur : Format de données incorrect - {str(e)}", "#ff6b6b")

    def context_supprimer(self):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, "values")
        if values and len(values) >= 3:
            employe_id, nom, prenom = values[0], values[1], values[2]
            self.supprimer_employe_direct(employe_id, nom, prenom)

    def modifier_employe_direct(self, employe_data):
        form = ModifierEmployeForm(self, employe_data)
        self.wait_window(form)
        
        if form.result:
            data = form.result
            try:
                modifier_employe(
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
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

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
        self.current_view = "tableau"
        self.ajout_btn.pack(side="right", padx=5, pady=5)
        self.search_frame.grid()
        
        try:
            conn = sqlite3.connect('employes.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE employes 
                SET id = (
                    SELECT COUNT(*) 
                    FROM employes AS e 
                    WHERE e.id <= employes.id
                )
            ''')
            conn.commit()
            
            cursor.execute('SELECT * FROM employes ORDER BY id')
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

    # =============== PLANNING MODERNISÉ (INSPIRÉ DE L'IMAGE) ===============
    def afficher_planning(self):
        self.current_view = "planning"
        self.ajout_btn.pack_forget()
        self.search_frame.grid_remove()

        for widget in self.tree_frame.winfo_children():
            widget.destroy()
        self.set_message("📅 Planning mensuel — Cliquez sur un jour pour gérer les affectations", "#6ecff6")

        if not hasattr(self, '_planning_date'):
            self._planning_date = datetime.now().replace(day=1)
        if not hasattr(self, '_selected_day'):
            self._selected_day = None

        current_date = self._planning_date
        year = current_date.year
        month = current_date.month
        today = datetime.today()

        # === Header personnalisé ===
        header_frame = tk.Frame(self.tree_frame, bg="#1e1e1e")
        header_frame.pack(fill="x", padx=15, pady=(0, 12))

        tk.Label(
            header_frame,
            text="Good morning, Admin",
            font=("Segoe UI", 16, "bold"),
            bg="#1e1e1e",
            fg="#e0e0e0"
        ).pack(side="left", padx=10)

        search_entry = tk.Entry(
            header_frame,
            font=("Segoe UI", 10),
            relief="flat",
            bg="#252526",
            fg="#e0e0e0",
            insertbackground="#4dabf7",
            highlightthickness=1,
            highlightbackground="#3c3c40",
            highlightcolor="#4dabf7",
            width=25
        )
        search_entry.insert(0, "🔍 Rechercher un employé...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, "end") if search_entry.get() == "🔍 Rechercher un employé..." else None)
        search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, "🔍 Rechercher un employé...") if not search_entry.get() else None)
        search_entry.pack(side="right", padx=10, ipady=4)

        # === Barre de navigation du planning ===
        nav_frame = tk.Frame(self.tree_frame, bg="#1e1e1e")
        nav_frame.pack(fill="x", padx=15, pady=(0, 12))

        tk.Button(
            nav_frame,
            text="◄",
            command=lambda: self._changer_mois(-1),
            font=("Segoe UI", 12, "bold"),
            bg="#3a3a3c",
            fg="#e0e0e0",
            relief="flat",
            cursor="hand2",
            width=3
        ).pack(side="left", padx=(0, 5))

        mois_fr = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
            5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        titre = f"{mois_fr[month]} {year}"
        tk.Label(
            nav_frame,
            text=titre,
            font=("Segoe UI", 15, "bold"),
            bg="#1e1e1e",
            fg="#e0e0e0"
        ).pack(side="left", padx=10)

        tk.Button(
            nav_frame,
            text="►",
            command=lambda: self._changer_mois(1),
            font=("Segoe UI", 12, "bold"),
            bg="#3a3a3c",
            fg="#e0e0e0",
            relief="flat",
            cursor="hand2",
            width=3
        ).pack(side="left", padx=(5, 20))

        tk.Button(
            nav_frame,
            text="Aujourd'hui",
            command=self._aller_a_aujourd_hui,
            font=("Segoe UI", 11, "bold"),
            bg="#4dabf7",
            fg="#121212",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=4
        ).pack(side="right")

        # === Layout principal : deux cartes horizontales ===
        main_frame = tk.Frame(self.tree_frame, bg="#1e1e1e")
        main_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        main_frame.grid_columnconfigure(0, weight=60)
        main_frame.grid_columnconfigure(1, weight=40)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Carte 1 : Calendrier ---
        cal_card = tk.Frame(main_frame, bg="#252526", bd=1, relief="flat")
        cal_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        cal_card.grid_propagate(False)

        tk.Label(
            cal_card,
            text="🗓️ Planning mensuel",
            font=("Segoe UI", 12, "bold"),
            bg="#252526",
            fg="#4dabf7",
            anchor="w",
            padx=12,
            pady=8
        ).pack(fill="x", side="top")

        cal_container = tk.Frame(cal_card, bg="#252526")
        cal_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        cal_container.grid_rowconfigure(0, weight=1)
        for i in range(7):
            cal_container.grid_columnconfigure(i, weight=1)

        jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for col, jour in enumerate(jours):
            tk.Label(
                cal_container,
                text=jour,
                font=("Segoe UI", 10, "bold"),
                bg="#2d2d2d",
                fg="#a0a0a0",
                height=2
            ).grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

        cal = calendar.monthcalendar(year, month)
        for row_idx, week in enumerate(cal, start=1):
            for col_idx, day in enumerate(week):
                if day == 0:
                    cell = tk.Frame(cal_container, bg="#252526")
                else:
                    is_today = (day == today.day and month == today.month and year == today.year)
                    is_selected = (self._selected_day == day and month == self._planning_date.month and year == self._planning_date.year)

                    if is_selected:
                        bg_color = "#6ecff6"
                        fg_color = "#121212"
                        font_weight = "bold"
                        highlight_bg = "#ffffff"
                    elif is_today:
                        bg_color = "#4dabf7"
                        fg_color = "#121212"
                        font_weight = "bold"
                        highlight_bg = "#ffffff"
                    else:
                        bg_color = "#2d2d2d"
                        fg_color = "#e0e0e0"
                        font_weight = "normal"
                        highlight_bg = "#3a3a3c"

                    cell = tk.Frame(
                        cal_container,
                        bg=bg_color,
                        highlightthickness=2,
                        highlightbackground=highlight_bg,
                        highlightcolor=highlight_bg,
                        cursor="hand2"
                    )

                    tk.Label(
                        cell,
                        text=str(day),
                        font=("Segoe UI", 11, font_weight),
                        bg=bg_color,
                        fg=fg_color
                    ).pack(expand=True, fill="both", padx=6, pady=8)

                    has_employees = (day % 5 == 0)
                    if has_employees:
                        indicator = tk.Label(
                            cell,
                            text="●",
                            font=("Segoe UI", 8),
                            bg=bg_color,
                            fg="#69db7c"
                        )
                        indicator.pack()

                    def on_enter(e, c=cell, orig_bg=bg_color):
                        if not (is_selected or is_today):
                            c.config(bg="#3a3a3c")
                    def on_leave(e, c=cell, orig_bg=bg_color):
                        if not (is_selected or is_today):
                            c.config(bg=orig_bg)

                    cell.bind("<Enter>", on_enter)
                    cell.bind("<Leave>", on_leave)
                    cell.bind("<Button-1>", lambda e, d=day: self._on_day_click(d, month, year))
                    for child in cell.winfo_children():
                        child.bind("<Button-1>", lambda e, d=day: self._on_day_click(d, month, year))

                cell.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="nsew")
                cal_container.grid_rowconfigure(row_idx, weight=1)

        # --- Carte 2 : Actions & Notifications ---
        actions_card = tk.Frame(main_frame, bg="#252526", bd=1, relief="flat")
        actions_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        actions_card.grid_propagate(False)

        tk.Label(
            actions_card,
            text="✨ Actions du jour",
            font=("Segoe UI", 12, "bold"),
            bg="#252526",
            fg="#4dabf7",
            anchor="w",
            padx=12,
            pady=8
        ).pack(fill="x", side="top")

        content_frame = tk.Frame(actions_card, bg="#252526")
        content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        info_frame = tk.Frame(content_frame, bg="#2d2d2d", relief="flat")
        info_frame.pack(fill="x", padx=8, pady=(8, 12))

        tk.Label(
            info_frame,
            text="📌 Cliquez sur un jour pour afficher les actions.",
            font=("Segoe UI", 10),
            bg="#2d2d2d",
            fg="#e0e0e0",
            padx=10,
            pady=8
        ).pack(fill="x", side="left")

        todo_frame = tk.Frame(content_frame, bg="#2d2d2d", relief="flat")
        todo_frame.pack(fill="x", padx=8, pady=(0, 12))

        tk.Label(
            todo_frame,
            text="✅ À faire aujourd'hui",
            font=("Segoe UI", 11, "bold"),
            bg="#2d2d2d",
            fg="#69db7c",
            padx=10,
            pady=6
        ).pack(fill="x", side="top")

        tasks = [
            "Ajouter un nouvel employé",
            "Vérifier les absences de la semaine",
            "Planifier les congés de décembre"
        ]

        for task in tasks:
            task_label = tk.Label(
                todo_frame,
                text=f"• {task}",
                font=("Segoe UI", 10),
                bg="#2d2d2d",
                fg="#e0e0e0",
                anchor="w",
                padx=15,
                pady=4
            )
            task_label.pack(fill="x", side="top", padx=5)

        self.planning_text = tk.Text(
            content_frame,
            bg="#1e1e1e",
            fg="#e0e0e0",
            font=("Segoe UI", 10),
            wrap="word",
            relief="flat",
            padx=12,
            pady=12,
            state="disabled"
        )
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=self.planning_text.yview)
        self.planning_text.configure(yscrollcommand=scrollbar.set)

        self.planning_text.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")

        self._update_planning_message(month, year)

    def _on_day_click(self, day, month, year):
        self._selected_day = day
        self._update_planning_message(month, year, selected_day=day)
        self.afficher_planning()

    def _update_planning_message(self, month, year, selected_day=None):
        message = ""
        if selected_day is not None:
            message = f"✅ Jour sélectionné :\n{selected_day} {self._get_month_name(month)} {year}\n\n"
            message += "• Affecter un employé\n• Marquer une absence\n• Voir les présences"
        else:
            message = "📆 Cliquez sur un jour\npour afficher les actions."

        self.planning_text.config(state="normal")
        self.planning_text.delete(1.0, "end")
        self.planning_text.insert("end", message)
        self.planning_text.config(state="disabled")

    def _get_month_name(self, month_num):
        mois_fr = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                   "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        return mois_fr[month_num]

    def _changer_mois(self, delta):
        if not hasattr(self, '_planning_date'):
            self._planning_date = datetime.now().replace(day=1)
        self._selected_day = None
        year = self._planning_date.year
        month = self._planning_date.month + delta
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
        self._planning_date = datetime(year, month, 1)
        self.afficher_planning()

    def _aller_a_aujourd_hui(self):
        self._planning_date = datetime.today().replace(day=1)
        self._selected_day = None
        self.afficher_planning()


def modifier_employe(employe_id, **kwargs):
    try:
        conn = sqlite3.connect('employes.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM employes WHERE id=?", (employe_id,))
        if not cursor.fetchone():
            raise ValueError(f"Employé avec ID {employe_id} introuvable")
        
        update_fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['nom', 'prenom'] and value.strip() == '':
                raise ValueError(f"Le champ {key} ne peut pas être vide")
            if key == 'age' and (not isinstance(value, int) or value < 16 or value > 65):
                raise ValueError("L'âge doit être entre 16 et 65 ans")
            if key == 'salaire':
                try:
                    sal = float(value)
                    if sal < 0:
                        raise ValueError("Le salaire doit être un nombre positif")
                    value = sal
                except ValueError:
                    raise ValueError("Le salaire doit être un nombre valide")
            
            update_fields.append(f"{key}=?")
            values.append(value)
        
        values.append(employe_id)
        query = f"UPDATE employes SET {', '.join(update_fields)} WHERE id=?"
        cursor.execute(query, values)
        conn.commit()
        return True
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        raise
    except ValueError as e:
        print(f"Erreur de validation: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    app = GestionEntiteApp()
    app.mainloop()
