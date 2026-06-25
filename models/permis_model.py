from config.database import Database

class PermisModel:
    def __init__(self):
        self.db = Database()

    def get_all_permis(self):
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT p.id_permis, p.numero_permis, p.date_delivrance, p.date_expiration,
                           pers.nom, pers.prenom
                    FROM permis_conduire p
                    JOIN personne pers ON p.id_personne = pers.id_personne
                """
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.db.close()

    def get_personnes(self):
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_personne, nom, prenom FROM personne")
                return cursor.fetchall()
        finally:
            self.db.close()

    def add_permis(self, numero, date_del, date_exp, id_personne):
        conn = self.db.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO permis_conduire (numero_permis, date_delivrance, date_expiration, id_personne)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (numero, date_del, date_exp, id_personne))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erreur permis : {e}")
            return False
        finally:
            self.db.close()