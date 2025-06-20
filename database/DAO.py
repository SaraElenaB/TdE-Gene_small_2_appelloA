from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                    FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    # -------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    # -------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllCromosomi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct g.Chromosome
                        from genes g 
                        order by g.Chromosome ASC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    # -------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllNodes(c1, c2, idMapGenes): #sono dei geni --> passare cromosomi
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT GeneID
                        FROM genes
                        WHERE Chromosome >= %s 
                        AND Chromosome <= %s"""
            cursor.execute(query, (c1, c2))

            for row in cursor:
                id_gene = row["GeneID"]
                if id_gene in idMapGenes:
                    result.extend(idMapGenes[id_gene])  #aggiunge gli elementi della lista singolarmente
                    #ti serve salvare singolarmente oggetti Gene, non liste perchè altrimenti nx non riesce ad aggiungere
                    #in quanto sono liste e non oggetti hashable

            print(f"Numero di nodi trovati da Python: {len(result)}")
            cursor.close()
            cnx.close()
        return result

    # -------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getEdgeWeight( g1Id, g2Id ):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select i.Expression_Corr as peso
                        from interactions i, classification c1, classification c2
                        where i.GeneID1 = %s
                        and i.GeneID2 = %s
                        and c1.GeneID = i.GeneID1
                        and c2.GeneID = i.GeneID2
                        and c1.Localization = c2.Localization"""
            cursor.execute(query, (g1Id, g2Id))

            for row in cursor:
                result.append(row["peso"])

            cursor.close()
            cnx.close()
        return result
    # -------------------------------------------------------------------------------------------------------------------------------
