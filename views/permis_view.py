import tkinter as tk
from tkinter import ttk

class PermisView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.set_view(self)
        self.create_widgets()

    def create_widgets(self):
        # Formulaire
        form_frame = tk.LabelFrame(self, text=" Nouveau Permis de Conduire ", padx=10, pady=10)
        form_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="N° Permis:").grid(row=0, column=0, sticky="w")
        self.entry_numero = tk.Entry(form_frame)
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Délivrance (AAAA-MM-JJ):").grid(row=0, column=2, sticky="w")
        self.entry_delivrance = tk.Entry(form_frame)
        self.entry_delivrance.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Expiration (AAAA-MM-JJ):").grid(row=1, column=2, sticky="w")
        self.entry_expiration = tk.Entry(form_frame)
        self.entry_expiration.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Titulaire:").grid(row=1, column=0, sticky="w")
        self.combo_personne = ttk.Combobox(form_frame, state="readonly")
        self.combo_personne.grid(row=1, column=1, padx=5, pady=5)

        btn_save = tk.Button(form_frame, text="Enregistrer", command=self.controller.save_permis, bg="#e67e22", fg="white")
        btn_save.grid(row=1, column=4, padx=10, pady=5)

        # Tableau
        table_frame = tk.LabelFrame(self, text=" Liste des Permis Délivrés ", padx=10, pady=10)
        table_frame.pack(side=tk.BOTTOM, fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=('id', 'numero', 'titulaire', 'delivrance', 'expiration'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('numero', text='N° Permis')
        self.tree.heading('titulaire', text='Titulaire')
        self.tree.heading('delivrance', text='Date Délivrance')
        self.tree.heading('expiration', text='Date Expiration')
        self.tree.pack(fill="both", expand=True)

        self.controller.load_data()

    def update_personnes(self, personnes):
        self.combo_personne['values'] = [f"{p['id_personne']} - {p['nom']} {p['prenom']}" for p in personnes]

    def update_table(self, data):
        for row in self.tree.get_children(): self.tree.delete(row)
        for p in data:
            self.tree.insert('', 'end', values=(p['id_permis'], p['numero_permis'], f"{p['nom']} {p['prenom']}", p['date_delivrance'], p['date_expiration']))