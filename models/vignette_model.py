from config.database import Database

class VignetteModel:
    def __init__(self):
        self.db = Database()

    def get_all_vehicules(self):
        """ Récupère la liste de tous les véhicules pour remplir la liste déroulante """
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                # Correction : Utilisation de 'md' au lieu du mot réservé 'mod'
                query = """
                    SELECT v.id_vehicule, v.immatriculation AS plaque_immatriculation, 
                           m.nom AS marque, md.libelle AS modele 
                    FROM vehicule v
                    INNER JOIN modele md ON v.id_modele = md.id_modele
                    INNER JOIN marque m ON md.id_marque = m.id_marque
                """
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.db.close()

    def get_all_vignettes(self):
        """ Récupère toutes les vignettes avec les informations nécessaires """
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                # Jointure complète pour récupérer l'immatriculation du véhicule et l'année fiscale
                query = """
                    SELECT v.id_vignette, v.numero_vignette, 
                           ex.annee, v.date_achat, cat.montant_vignette AS prix, 
                           v.id_vehicule, veh.immatriculation AS plaque_immatriculation,
                           cat.libelle AS type_vignette
                    FROM vignette v
                    INNER JOIN vehicule veh ON v.id_vehicule = veh.id_vehicule
                    INNER JOIN exercice_fiscal ex ON v.id_exercice = ex.id_exercice
                    INNER JOIN categorie_vehicule cat ON veh.id_categorie = cat.id_categorie
                """
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.db.close()

    def get_exercice_par_annee(self, annee):
        """ Récupère l'id_exercice correspondant à une année donnée """
        conn = self.db.connect()
        if not conn: return None
        try:
            with conn.cursor() as cursor:
                query = "SELECT id_exercice FROM exercice_fiscal WHERE annee = %s"
                cursor.execute(query, (annee,))
                res = cursor.fetchone()
                return res['id_exercice'] if res else None
        finally:
            self.db.close()

    def add_vignette(self, numero_vignette, annee, date_achat, id_vehicule):
        """ Enregistre une nouvelle vignette """
        # 1. On cherche l'ID de l'exercice fiscal correspondant à l'année saisie
        id_exercice = self.get_exercice_par_annee(annee)
        if not id_exercice:
            print(f"Erreur : L'exercice fiscal pour l'année {annee} n'existe pas dans la base.")
            return False

        conn = self.db.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO vignette (numero_vignette, date_achat, id_vehicule, id_exercice)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (numero_vignette, date_achat, id_vehicule, id_exercice))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erreur d'insertion de la vignette : {e}")
            return False
        finally:
            self.db.close()