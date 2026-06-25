from config.database import Database

class VignetteModel:
    def __init__(self):
        self.db = Database()

    def get_all_vignettes(self):
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                # Jointure pour afficher des infos claires (Immatriculation et Année fiscale)
                query = """
                    SELECT v.id_vignette, v.numero_vignette, v.date_achat, 
                           veh.immatriculation, ex.annee
                    FROM vignette v
                    JOIN vehicule veh ON v.id_vehicule = veh.id_vehicule
                    JOIN exercice_fiscal ex ON v.id_exercice = ex.id_exercice
                """
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.db.close()

    def get_vehicules(self):
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_vehicule, immatriculation FROM vehicule")
                return cursor.fetchall()
        finally:
            self.db.close()

    def get_exercices(self):
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_exercice, annee FROM exercice_fiscal")
                return cursor.fetchall()
        finally:
            self.db.close()

    def add_vignette(self, numero, date_achat, id_vehicule, id_exercice):
        conn = self.db.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO vignette (numero_vignette, date_achat, id_vehicule, id_exercice)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (numero, date_achat, id_vehicule, id_exercice))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erreur vignette : {e}")
            return False
        finally:
            self.db.close()