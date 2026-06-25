from tkinter import messagebox

class PermisController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view

    def load_data(self):
        permis = self.model.get_all_permis()
        personnes = self.model.get_personnes()
        if self.view:
            self.view.update_personnes(personnes)
            self.view.update_table(permis)

    def save_permis(self):
        num = self.view.entry_numero.get()
        date_d = self.view.entry_delivrance.get()
        date_e = self.view.entry_expiration.get()
        pers_sel = self.view.combo_personne.get()

        if not num or not date_d or not date_e or not pers_sel:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        id_personne = int(pers_sel.split(" - ")[0])

        if self.model.add_permis(num, date_d, date_e, id_personne):
            messagebox.showinfo("Succès", "Permis de conduire enregistré !")
            self.load_data()
            self.view.entry_numero.delete(0, 'end')
            self.view.entry_delivrance.delete(0, 'end')
            self.view.entry_expiration.delete(0, 'end')
        else:
            messagebox.showerror("Erreur", "Échec de l'enregistrement.")