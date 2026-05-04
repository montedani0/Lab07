from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def umidita_media(mese):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.Localita  , AVG(s.Umidita ) as media
                        from situazione s
                        where MONTH(s.`Data`) = %s
                        group by s.Localita  """
            res = {}
            cursor.execute(query,(mese,))
            for row in cursor:
                res[row["Localita"]] = row["media"]
            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def spesa(mese):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select  day(s.`Data`) as d ,s.Localita ,s.Umidita 
                        from situazione s
                        where MONTH(s.`Data`) = %s and DAY(s.`Data` )<=15
                        ORDER BY s.Data, s.Localita
                        """
            res = {}
            cursor.execute(query, (mese,))
            for row in cursor:
                res[(row["Localita"], row["d"])] = row["Umidita"]
            cursor.close()
            cnx.close()
            return res



