from config.database import Database

class PersonneModel:
    def __init__(self):
        self.db = Database()

    def get_all_personnes(self):
        conn = self.db.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                # Ajout de tous les champs nécessaires pour la modification (sexe, adresse, date...)
                query = """
                    SELECT id_personne, nom, postnom, prenom, 
                           date_naissance, sexe, lieu_naissance, adresse, telephone 
                    FROM personne
                """
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

    def update_personne(self, id_personne, nom, postnom, prenom, date_naiss, sexe, lieu_naiss, adresse, telephone):
        """ Met à jour les informations d'un citoyen existant """
        conn = self.db.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                query = """
                    UPDATE personne 
                    SET nom = %s, postnom = %s, prenom = %s, date_naissance = %s, 
                        sexe = %s, lieu_naissance = %s, adresse = %s, telephone = %s
                    WHERE id_personne = %s
                """
                cursor.execute(query, (nom, postnom, prenom, date_naiss, sexe, lieu_naiss, adresse, telephone, id_personne))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erreur de modification : {e}")
            return False
        finally:
            self.db.close()

    def delete_personne(self, id_personne):
        """ Supprime définitivement une personne de la base de données """
        conn = self.db.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                query = "DELETE FROM personne WHERE id_personne = %s"
                cursor.execute(query, (id_personne,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erreur de suppression : {e}")
            return False
        finally:
            self.db.close()