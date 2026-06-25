import tkinter as tk
from tkinter import ttk, messagebox


class PersonneView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.set_view(self)

        self.create_widgets()

    def create_widgets(self):
        # --- Formulaire d'ajout ---
        form_frame = tk.LabelFrame(self, text=" Ajouter une Personne ", padx=10, pady=10)
        form_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(form_frame, text="Nom:").grid(row=0, column=0, sticky="w")
        self.entry_nom = tk.Entry(form_frame)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Prénom:").grid(row=0, column=2, sticky="w")
        self.entry_prenom = tk.Entry(form_frame)
        self.entry_prenom.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Téléphone:").grid(row=1, column=0, sticky="w")
        self.entry_phone = tk.Entry(form_frame)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        btn_valider = tk.Button(form_frame, text="Enregistrer", command=self.controller.save_personne, bg="#2ecc71",
                                fg="white")
        btn_valider.grid(row=1, column=3, padx=5, pady=5, sticky="e")

        # --- Tableau d'affichage (Treeview) ---
        table_frame = tk.LabelFrame(self, text=" Liste des Personnes ", padx=10, pady=10)
        table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ('id', 'nom', 'postnom', 'prenom', 'telephone')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        self.tree.heading('id', text='ID')
        self.tree.heading('nom', text='Nom')
        self.tree.heading('postnom', text='Postnom')
        self.tree.heading('prenom', text='Prénom')
        self.tree.heading('telephone', text='Téléphone')

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Charger les données initiales
        self.controller.load_data()

    def update_table(self, data):
        # Vider le tableau
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Remplir le tableau
        for p in data:
            self.tree.insert('', tk.END,
                             values=(p['id_personne'], p['nom'], p.get('postnom', ''), p['prenom'], p['telephone']))