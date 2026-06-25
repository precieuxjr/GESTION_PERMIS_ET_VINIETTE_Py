from config.database import Database

class PersonneModel:
    def __init__(self):
        self.db = Database()

    def get_all_personnes(self):
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                query = "SELECT id_personne, nom, postnom, prenom, telephone FROM personne"
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.db.close()

    def add_personne(self, nom, postnom, prenom, date_naiss, sexe, lieu_naiss, adresse, telephone):
        conn = self.db.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO personne (nom, postnom, prenom, date_naissance, sexe, lieu_naissance, adresse, telephone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nom, postnom, prenom, date_naiss, sexe, lieu_naiss, adresse, telephone))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erreur d'insertion : {e}")
            return False
        finally:
            self.db.close()