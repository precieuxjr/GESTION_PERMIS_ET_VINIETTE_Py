from tkinter import messagebox
from datetime import datetime

class PersonneController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view

    def load_data(self):
        """ Récupère l'ensemble des données depuis le modèle et actualise la vue """
        data = self.model.get_all_personnes()
        if self.view:
            self.view.update_table(data)

    def save_personne(self):
        """ Gère l'enregistrement (Ajout ou Modification) d'un citoyen """
        # Récupération des valeurs depuis la vue
        nom = self.view.entry_nom.get().strip()
        postnom = self.view.entry_postnom.get().strip()
        prenom = self.view.entry_prenom.get().strip()
        phone = self.view.entry_phone.get().strip()
        sexe = self.view.combo_sexe.get()
        adresse = self.view.entry_adresse.get().strip()

        # Vérifications de base (Champs obligatoires)
        if not nom or not prenom or not phone or not sexe:
            messagebox.showerror("Champs requis", "Veuillez remplir les champs obligatoires (*).")
            return

        # Extraction et formatage de la date depuis le DateEntry
        try:
            date_naiss = self.view.entry_date_naiss.get_date().strftime('%Y-%m-%d')
        except Exception:
            date_naiss = None

        if self.view.selected_personne_id is None:
            # --- MODE CRÉATION ---
            success = self.model.add_personne(nom, postnom, prenom, date_naiss, sexe, "", adresse, phone)
            message = "Personne ajoutée avec succès !"
        else:
            # --- MODE MODIFICATION ---
            success = self.model.update_personne(self.view.selected_personne_id, nom, postnom, prenom, date_naiss, sexe,
                                                 "", adresse, phone)
            message = "Informations mises à jour avec succès !"

        if success:
            messagebox.showinfo("Succès", message)
            self.view.reset_form()
            self.load_data()  # Recharge et réaffiche les lignes immédiatement
        else:
            messagebox.showerror("Erreur", "L'opération a échoué. Vérifiez vos données de connexion.")

    def on_row_double_click(self, event):
        """ Se déclenche lors d'un double-clic sur une ligne du tableau pour passer en mode édition """
        selected_item = self.view.tree.selection()
        if not selected_item:
            return

        # Récupération des valeurs de la ligne sélectionnée
        values = self.view.tree.item(selected_item, 'values')

        # Passage du formulaire en mode édition
        self.view.selected_personne_id = int(values[0])
        self.view.form_frame.config(text=" ✏️ MODIFIER LE CITOYEN ", fg="#e67e22")
        self.view.btn_enregistrer.config(text="💾 Mettre à jour", bg="#e67e22")
        self.view.btn_supprimer.pack(side="left", padx=5)  # Affiche le bouton supprimer

        # Remplissage des champs textuels simples
        self.view.entry_nom.delete(0, 'end')
        self.view.entry_nom.insert(0, values[1])

        self.view.entry_postnom.delete(0, 'end')
        self.view.entry_postnom.insert(0, values[2])

        self.view.entry_prenom.delete(0, 'end')
        self.view.entry_prenom.insert(0, values[3])

        self.view.combo_sexe.set(values[4])

        self.view.entry_phone.delete(0, 'end')
        self.view.entry_phone.insert(0, values[5])

        # Adaptation du DateEntry pour afficher la date de la ligne sélectionnée
        date_str = values[6]
        if date_str and date_str != 'None' and date_str.strip() != '':
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                self.view.entry_date_naiss.set_date(date_obj)
            except ValueError:
                # Si le format reçu est corrompu, on remet la date du jour par défaut
                self.view.entry_date_naiss.set_date(self.view.entry_date_naiss.datetime.today())
        else:
            self.view.entry_date_naiss.set_date(self.view.entry_date_naiss.datetime.today())

        self.view.entry_adresse.delete(0, 'end')
        self.view.entry_adresse.insert(0, values[7])

    def delete_personne(self):
        """ Supprime l'enregistrement actuellement sélectionné """
        pid = self.view.selected_personne_id
        if pid is None:
            return

        confirm = messagebox.askyesno("Confirmation",
                                      "Êtes-vous sûr de vouloir supprimer définitivement cette personne ?")
        if confirm:
            if self.model.delete_personne(pid):
                messagebox.showinfo("Supprimé", "L'enregistrement a bien été effacé.")
                self.view.reset_form()
                self.load_data()  # Force l'actualisation visuelle
            else:
                messagebox.showerror("Erreur",
                                     "Impossible de supprimer cette personne. Elle est probablement liée à un permis ou un véhicule actif.")