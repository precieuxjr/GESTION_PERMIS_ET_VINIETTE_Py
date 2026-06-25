from tkinter import messagebox


class PersonneController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view

    def load_data(self):
        data = self.model.get_all_personnes()
        if self.view:
            self.view.update_table(data)

    def save_personne(self):
        nom = self.view.entry_nom.get()
        prenom = self.view.entry_prenom.get()
        phone = self.view.entry_phone.get()

        if not nom or not prenom:
            messagebox.showerror("Erreur", "Le nom et le prénom sont obligatoires.")
            return

        # Appel au modèle pour l'insertion (Ici avec des valeurs par défaut pour simplifier le test rapide)
        success = self.model.add_personne(nom, "", prenom, "2000-01-01", "M", "Kinshasa", "Adresse de test", phone)

        if success:
            messagebox.showinfo("Succès", "Personne ajoutée avec succès !")
            self.load_data()  # Rafraîchir le tableau
            # Nettoyer les champs
            self.view.entry_nom.delete(0, tk.END)
            self.view.entry_prenom.delete(0, tk.END)
            self.view.entry_phone.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Impossible d'enregistrer la personne.")