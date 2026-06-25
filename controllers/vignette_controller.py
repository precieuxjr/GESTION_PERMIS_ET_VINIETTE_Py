from tkinter import messagebox


class VignetteController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view

    def populate_vehicules(self):
        """ Charge la liste des véhicules dans la vue """
        vehicules = self.model.get_all_vehicules()
        if self.view:
            self.view.update_vehicules_combobox(vehicules)

    def save_vignette(self):
        numero = self.view.entry_numero.get().strip()
        type_v = self.view.combo_type.get()
        annee = self.view.entry_annee.get().strip()
        prix = self.view.entry_prix.get().strip()

        # Récupération du texte sélectionné dans la Combobox
        vehicule_selectionne = self.view.combo_vehicule.get()

        # Validation
        if not numero or not type_v or not annee or not prix or not vehicule_selectionne:
            messagebox.showerror("Champs requis", "Veuillez remplir tous les champs obligatoires (*).")
            return

        # Extraction de l'ID du véhicule via la Map
        id_vehicule = self.view.vehicules_map.get(vehicule_selectionne)

        date_achat = self.view.entry_date_achat.get_date().strftime('%Y-%m-%d')

        # Insertion en BDD
        success = self.model.add_vignette(numero, type_v, annee, date_achat, prix, id_vehicule)

        if success:
            messagebox.showinfo("Succès", "La vignette a bien été enregistrée pour ce véhicule !")
            # Réinitialiser les champs ici...
        else:
            messagebox.showerror("Erreur", "Une erreur est survenue lors de l'enregistrement.")