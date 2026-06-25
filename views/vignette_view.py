import tkinter as tk
from tkinter import ttk

class VignetteView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.set_view(self)
        self.create_widgets()

    def create_widgets(self):
        # Formulaire
        form_frame = tk.LabelFrame(self, text=" Acheter une Vignette ", padx=10, pady=10)
        form_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="N° Vignette:").grid(row=0, column=0, sticky="w")
        self.entry_numero = tk.Entry(form_frame)
        self.entry_numero.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Date (AAAA-MM-JJ):").grid(row=0, column=2, sticky="w")
        self.entry_date = tk.Entry(form_frame)
        self.entry_date.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Véhicule:").grid(row=1, column=0, sticky="w")
        self.combo_vehicule = ttk.Combobox(form_frame, state="readonly")
        self.combo_vehicule.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Exercice Fiscal:").grid(row=1, column=2, sticky="w")
        self.combo_exercice = ttk.Combobox(form_frame, state="readonly")
        self.combo_exercice.grid(row=1, column=3, padx=5, pady=5)

        btn_save = tk.Button(form_frame, text="Enregistrer", command=self.controller.save_vignette, bg="#3498db", fg="white")
        btn_save.grid(row=1, column=4, padx=10, pady=5)

        # Tableau
        table_frame = tk.LabelFrame(self, text=" Historique des Vignettes ", padx=10, pady=10)
        table_frame.pack(side=tk.BOTTOM, fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=('id', 'numero', 'date', 'vehicule', 'exercice'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('numero', text='N° Vignette')
        self.tree.heading('date', text='Date Achat')
        self.tree.heading('vehicule', text='Véhicule (Immatriculation)')
        self.tree.heading('exercice', text='Exercice Fiscal')
        self.tree.pack(fill="both", expand=True)

        self.controller.load_data()

    def update_lists(self, vehicules, exercices):
        self.combo_vehicule['values'] = [f"{v['id_vehicule']} - {v['immatriculation']}" for v in vehicules]
        self.combo_exercice['values'] = [f"{e['id_exercice']} - {e['annee']}" for e in exercices]

    def update_table(self, data):
        for row in self.tree.get_children(): self.tree.delete(row)
        for v in data:
            self.tree.insert('', 'end', values=(v['id_vignette'], v['numero_vignette'], v['date_achat'], v['immatriculation'], v['annee']))