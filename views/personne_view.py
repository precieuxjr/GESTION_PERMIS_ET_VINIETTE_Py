import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # <-- Importation du calendrier interactif


class PersonneView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        self.controller.set_view(self)

        # Variable pour suivre la personne en cours de modification (None si nouvel ajout)
        self.selected_personne_id = None

        self.create_widgets()

    def create_widgets(self):
        # Enregistrement de la fonction de validation pour les entiers
        vcmd = (self.register(self.validate_numeric), '%P')

        # --- Formulaire d'ajout / Modification ---
        self.form_frame = tk.LabelFrame(self, text=" ENREGISTRER UN NOUVEAU CITOYEN ",
                                        font=("Segoe UI", 10, "bold"), fg="#1e90ff",
                                        bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        self.form_frame.pack(side=tk.TOP, fill="x", padx=20, pady=10)

        lbl_style = {"bg": "#ffffff", "fg": "#2f3542", "font": ("Segoe UI", 10)}
        entry_style = {"font": ("Segoe UI", 10), "bd": 1, "relief": "solid"}

        # Ligne 1 : Nom, Postnom, Prénom
        tk.Label(self.form_frame, text="Nom *:", **lbl_style).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nom = tk.Entry(self.form_frame, width=20, **entry_style)
        self.entry_nom.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Postnom:", **lbl_style).grid(row=0, column=2, sticky="w", pady=5)
        self.entry_postnom = tk.Entry(self.form_frame, width=20, **entry_style)
        self.entry_postnom.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(self.form_frame, text="Prénom *:", **lbl_style).grid(row=0, column=4, sticky="w", pady=5)
        self.entry_prenom = tk.Entry(self.form_frame, width=20, **entry_style)
        self.entry_prenom.grid(row=0, column=5, padx=10, pady=5)

        # Ligne 2 : Téléphone (Validé), Sexe, Date Naissance (DateEntry)
        tk.Label(self.form_frame, text="Téléphone *:", **lbl_style).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_phone = tk.Entry(self.form_frame, width=20, validate="key", validatecommand=vcmd, **entry_style)
        self.entry_phone.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Sexe *:", **lbl_style).grid(row=1, column=2, sticky="w", pady=5)
        self.combo_sexe = ttk.Combobox(self.form_frame, values=["M", "F"], width=18, state="readonly")
        self.combo_sexe.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(self.form_frame, text="Né(e) le *:", **lbl_style).grid(row=1, column=4, sticky="w", pady=5)
        self.entry_date_naiss = DateEntry(self.form_frame, width=19, font=("Segoe UI", 10),
                                          background='#1e90ff', foreground='white',
                                          borderwidth=1, relief="solid",
                                          date_pattern='yyyy-mm-dd')
        self.entry_date_naiss.grid(row=1, column=5, padx=10, pady=5)

        # Ligne 3 : Adresse
        tk.Label(self.form_frame, text="Adresse:", **lbl_style).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_adresse = tk.Entry(self.form_frame, width=53, **entry_style)
        self.entry_adresse.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="w")

        # --- Zone des Boutons d'action ---
        btn_frame = tk.Frame(self.form_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=4, columnspan=2, sticky="e", pady=5)

        self.btn_enregistrer = tk.Button(btn_frame, text="💾 Enregistrer", command=self.controller.save_personne,
                                         font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", bd=0, cursor="hand2",
                                         padx=10, pady=4)
        self.btn_enregistrer.pack(side=tk.LEFT, padx=5)

        self.btn_annuler = tk.Button(btn_frame, text="🔄 Annuler", command=self.reset_form,
                                     font=("Segoe UI", 10, "bold"), bg="#718093", fg="white", bd=0, cursor="hand2",
                                     padx=10, pady=4)
        self.btn_annuler.pack(side=tk.LEFT, padx=5)

        self.btn_supprimer = tk.Button(btn_frame, text="🗑️ Supprimer", command=self.controller.delete_personne,
                                       font=("Segoe UI", 10, "bold"), bg="#e74c3c", fg="white", bd=0, cursor="hand2",
                                       padx=10, pady=4)
        self.btn_supprimer.pack(side=tk.LEFT, padx=5)
        self.btn_supprimer.pack_forget()

        # --- Tableau d'affichage (Treeview) ---
        table_frame = tk.LabelFrame(self, text=" LISTE DES PERSONNES (Double-cliquez pour modifier) ",
                                    font=("Segoe UI", 10, "bold"), fg="#718093", bg="#ffffff", bd=0)
        table_frame.pack(side=tk.BOTTOM, fill="both", expand=True, padx=20, pady=10)

        # --- AJOUT DU BOUTON ACTUALISER ---
        top_table_bar = tk.Frame(table_frame, bg="#ffffff")
        top_table_bar.pack(side=tk.TOP, fill="x", pady=5)

        self.btn_actualiser = tk.Button(top_table_bar, text="🔄 Actualiser la liste", command=self.controller.load_data,
                                        font=("Segoe UI", 9, "bold"), bg="#3498db", fg="white", bd=0, cursor="hand2",
                                        padx=12, pady=4)
        self.btn_actualiser.pack(side=tk.RIGHT, padx=5)

        # --- Fin de la zone d'actualisation ---

        columns = ('id', 'nom', 'postnom', 'prenom', 'sexe', 'telephone', 'date_naiss', 'adresse')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        self.tree.heading('id', text='ID')
        self.tree.heading('nom', text='Nom')
        self.tree.heading('postnom', text='Postnom')
        self.tree.heading('prenom', text='Prénom')
        self.tree.heading('sexe', text='Sexe')
        self.tree.heading('telephone', text='Téléphone')
        self.tree.heading('date_naiss', text='Date Naiss.')
        self.tree.heading('adresse', text='Adresse')

        self.tree.column('id', width=40, anchor="center")
        self.tree.column('sexe', width=40, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.tree.bind("<Double-1>", self.controller.on_row_double_click)

        self.controller.load_data()

    def validate_numeric(self, current_value):
        if current_value == "" or current_value.isdigit():
            return True
        return False

    def reset_form(self):
        """ Réinitialise le formulaire à son état d'origine """
        self.selected_personne_id = None
        self.form_frame.config(text=" ENREGISTRER UN NOUVEAU CITOYEN ", fg="#1e90ff")
        self.btn_enregistrer.config(text="💾 Enregistrer", bg="#2ecc71")
        self.btn_supprimer.pack_forget()

        # Nettoyage des champs
        self.entry_nom.delete(0, tk.END)
        self.entry_postnom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.combo_sexe.set('')
        self.entry_adresse.delete(0, tk.END)

        # Réinitialisation du calendrier à la date courante du jour
        self.entry_date_naiss.set_date(self.entry_date_naiss.datetime.today())

    def update_table(self, data):
        """ Vide le tableau et réinsère les données fraîches en forçant le rendu visuel """
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in data:
            date_naiss_raw = p.get('date_naissance')
            if date_naiss_raw and not isinstance(date_naiss_raw, str):
                date_naiss_str = date_naiss_raw.strftime('%Y-%m-%d')
            else:
                date_naiss_str = date_naiss_raw or ''

            self.tree.insert('', tk.END, values=(
                p['id_personne'],
                p['nom'],
                p.get('postnom') or '',
                p['prenom'],
                p.get('sexe') or '',
                p['telephone'],
                date_naiss_str,
                p.get('adresse') or ''
            ))

        self.update_idletasks()