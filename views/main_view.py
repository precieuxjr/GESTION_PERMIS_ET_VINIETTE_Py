import tkinter as tk
from tkinter import ttk

from models.personne_model import PersonneModel
from controllers.personne_controller import PersonneController
from views.personne_view import PersonneView

from models.vignette_model import VignetteModel
from controllers.vignette_controller import VignetteController
from views.vignette_view import VignetteView

from models.permis_model import PermisModel
from controllers.permis_controller import PermisController
from views.permis_view import PermisView


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Système de Gestion Automobile")
        self.geometry("1100x700")
        self.configure(bg="#f1f2f6")  # Fond général de la fenêtre

        # --- CONFIGURATION DU STYLE TTK ---
        style = ttk.Style()
        style.theme_use('clam')  # Un thème de base plus moderne que l'original

        # Configuration des Onglets (Notebook)
        style.configure("TNotebook", background="#f1f2f6", borderwidth=0)
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 11, "bold"),
                        padding=[15, 8],
                        background="#dcdde1",
                        foreground="#2f3542")
        style.map("TNotebook.Tab",
                  background=[("selected", "#ffffff")],
                  foreground=[("selected", "#1e90ff")])

        # Style pour les tableaux (Treeview)
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=25,
                        background="#ffffff",
                        fieldbackground="#ffffff")
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#718093",
                        foreground="white")
        style.map("Treeview.Heading", background=[('active', '#2f3542')])

        # Système d'onglets
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Instanciation des modules
        p_model = PersonneModel()
        p_controller = PersonneController(p_model)
        tab_personne = PersonneView(notebook, p_controller)
        notebook.add(tab_personne, text=" Gestion Citoyens ")

        v_model = VignetteModel()
        v_controller = VignetteController(v_model)
        tab_vignette = VignetteView(notebook, v_controller)
        notebook.add(tab_vignette, text=" Gestion des Vignettes ")

        perm_model = PermisModel()
        perm_controller = PermisController(perm_model)
        tab_permis = PermisView(notebook, perm_controller)
        notebook.add(tab_permis, text="  Permis de Conduire ")