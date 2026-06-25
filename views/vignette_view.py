import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class VignetteView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        self.controller.set_view(self)

        # Dictionnaire pour mapper le texte de la combobox à l'ID réel du véhicule
        self.vehicules_map = {}

        self.create_widgets()

    def create_widgets(self):
        self.form_frame = tk.LabelFrame(self, text=" ENREGISTRER UNE VIGNETTE ",
                                        font=("Segoe UI", 10, "bold"), fg="#1e90ff",
                                        bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        self.form_frame.pack(side=tk.TOP, fill="x", padx=20, pady=10)

        lbl_style = {"bg": "#ffffff", "fg": "#2f3542", "font": ("Segoe UI", 10)}
        entry_style = {"font": ("Segoe UI", 10), "bd": 1, "relief": "solid"}

        # Ligne 1 : Numéro de Vignette, Type, Année
        tk.Label(self.form_frame, text="N° Vignette *:", **lbl_style).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_numero = tk.Entry(self.form_frame, width=20, **entry_style)
        self.entry_numero.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Type *:", **lbl_style).grid(row=0, column=2, sticky="w", pady=5)
        self.combo_type = ttk.Combobox(self.form_frame, values=["Physique", "Virtuelle"], width=18, state="readonly")
        self.combo_type.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(self.form_frame, text="Année *:", **lbl_style).grid(row=0, column=4, sticky="w", pady=5)
        self.entry_annee = tk.Entry(self.form_frame, width=20, **entry_style)
        self.entry_annee.grid(row=0, column=5, padx=10, pady=5)

        # Ligne 2 : Date Achat, Prix, SÉLECTION VÉHICULE
        tk.Label(self.form_frame, text="Date d'achat *:", **lbl_style).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_date_achat = DateEntry(self.form_frame, width=19, font=("Segoe UI", 10),
                                          background='#1e90ff', foreground='white',
                                          borderwidth=1, relief="solid", date_pattern='yyyy-mm-dd')
        self.entry_date_achat.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.form_frame, text="Prix (USD) *:", **lbl_style).grid(row=1, column=2, sticky="w", pady=5)
        self.entry_prix = tk.Entry(self.form_frame, width=20, **entry_style)
        self.entry_prix.grid(row=1, column=3, padx=10, pady=5)

        # Liste déroulante des véhicules
        tk.Label(self.form_frame, text="Véhicule *:", **lbl_style).grid(row=1, column=4, sticky="w", pady=5)
        self.combo_vehicule = ttk.Combobox(self.form_frame, width=18, state="readonly")
        self.combo_vehicule.grid(row=1, column=5, padx=10, pady=5)

        # Bouton d'action
        self.btn_enregistrer = tk.Button(self.form_frame, text="💾 Enregistrer", command=self.controller.save_vignette,
                                         font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", bd=0, cursor="hand2",
                                         padx=15, pady=4)
        self.btn_enregistrer.grid(row=2, column=5, sticky="e", pady=10, padx=10)

        # --- On charge directement les véhicules dans la combobox ---
        self.controller.populate_vehicules()

    def update_vehicules_combobox(self, vehicules):
        """ Remplit la combobox avec les véhicules de la BDD """
        combobox_values = []
        self.vehicules_map.clear()

        for v in vehicules:
            # On construit une chaîne lisible
            display_text = f"ID: {v['id_vehicule']} | {v['plaque_immatriculation']} ({v['marque']})"
            combobox_values.append(display_text)
            # On stocke l'ID correspondant au texte sélectionné
            self.vehicules_map[display_text] = v['id_vehicule']

        self.combo_vehicule['values'] = combobox_values