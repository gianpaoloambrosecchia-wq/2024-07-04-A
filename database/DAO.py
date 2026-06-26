from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.datetime) as year
                    from sighting s
                    order by year(s.datetime) desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getShapesForYear(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape 
                    from sighting s 
                    where year(s.`datetime`) = %s and s.shape != ""
                    order by s.shape asc"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllNodes(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.*
                    from sighting s 
                    where year(s.`datetime`) = %s and s.shape = %s"""
            cursor.execute(query, (year, shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllEdges(year, shape, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as s1id, s2.id as s2id
                    from (select distinct s.*
                    from sighting s 
                    where year(s.`datetime`) = %s and s.shape = %s) s1
                    join (select distinct s.*
                    from sighting s 
                    where year(s.`datetime`) = %s and s.shape = %s) s2 on s1.state = s2.state
                    where s1.id < s2.id """
            cursor.execute(query, (year, shape, year, shape))

            for row in cursor:
                result.append((
                    idMap[row["s1id"]],
                    idMap[row["s2id"]]
                ))
            cursor.close()
            cnx.close()
        return result