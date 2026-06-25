from tkinter import messagebox


class VignetteController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view

    def load_data(self):
        vignettes = self.model.get_all_vignettes()
        vehicules = self.model.get_vehicules()
        exercices = self.model.get_exercices()

        if self.view:
            self.view.update_lists(vehicules, exercices)
            self.view.update_table(vignettes)

    def save_vignette(self):
        num = self.view.entry_numero.get()
        date_a = self.view.entry_date.get()
        veh_sel = self.view.combo_vehicule.get()
        exe_sel = self.view.combo_exercice.get()

        if not num or not date_a or not veh_sel or not exe_sel:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        # Extraction des IDs depuis le texte des ComboBox (ex: "1 - 1234AB01" -> 1)
        id_vehicule = int(veh_sel.split(" - ")[0])
        id_exercice = int(exe_sel.split(" - ")[0])

        if self.model.add_vignette(num, date_a, id_vehicule, id_exercice):
            messagebox.showinfo("Succès", "Vignette enregistrée avec succès !")
            self.load_data()
            self.view.entry_numero.delete(0, 'end')
            self.view.entry_date.delete(0, 'end')
        else:
            messagebox.showerror("Erreur", "Échec de l'enregistrement.")