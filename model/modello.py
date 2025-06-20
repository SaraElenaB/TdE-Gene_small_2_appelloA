import copy

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []

        self._genes = DAO.get_all_genes()

        self._idMapGenes = {} #{'idGene1': [g1, g2], 'idGene2': [g4, g1], 'key3': []}
        for gene in self._genes:
            if gene.GeneID in self._idMapGenes.keys():
                self._idMapGenes[gene.GeneID].append(gene)
            else:
                self._idMapGenes[gene.GeneID] = [gene]

        self._interaction = DAO.get_all_interactions()

        self._bestPath = []
        self._bestScore = 100000000000000

    # -------------------------------------------------------------------------------------------------------------------------------
    def getAllCromosomi(self):
        return DAO.getAllCromosomi()

    def getIdMapGenes(self):
        return self._idMapGenes

    def getInteraction(self):
        return self._interaction

    # -------------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, c1, c2):

        self._grafo.clear()
        self._nodes = DAO.getAllNodes(c1, c2, self._idMapGenes)
        print( len(self._nodes) )
        self._grafo.add_nodes_from(self._nodes)

        mapNodi = {}
        for g in self._nodes:
            geneId = g.GeneID
            if geneId not in mapNodi:
                mapNodi[g.GeneID] = [g]
            else:
                mapNodi[g.GeneID].append(g)

        for inter in self._interaction:
            gene1 = mapNodi.get(inter.GeneID1)
            gene2 = mapNodi.get(inter.GeneID2)

            if gene1 is not None and gene2 is not None:
                peso = DAO.getEdgeWeight(inter.GeneID1, inter.GeneID2)
                if peso is not None and len(peso) > 0:
                    for g1 in gene1:
                        for g2 in gene2:
                            if g1.GeneID != g2.GeneID:
                                if g1.Chromosome < g2.Chromosome:
                                    self._grafo.add_edge(g1, g2, weight=peso[0])
                                elif g1.Chromosome > g2.Chromosome:
                                    self._grafo.add_edge(g2, g1, weight=peso[0])
                                elif g1.Chromosome == g2.Chromosome:
                                    self._grafo.add_edge(g1, g2, weight=peso[0])
                                    self._grafo.add_edge(g2, g1, weight=peso[0])

        return self._grafo

    def getDetailsGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # -------------------------------------------------------------------------------------------------------------------------------
    def getMaxNodi(self):

        lista = []    #lista= [ (nodo1, numUscenti) , (nodo2, numUscenti)]
        nodiGiaVisti = []

        for n in self._nodes:
            if n not in nodiGiaVisti:
                nodiGiaVisti.append(n)
                numUscenti = 0
                pesoTot = 0
                for succ in self._grafo.successors(n):
                    numUscenti += 1
                    pesoTot += self._grafo[n][succ]['weight']
                lista.append( (n, numUscenti, pesoTot ) )
            else:
                continue

        lista.sort( key=lambda x: x[1], reverse=True)
        return lista[:5]

    # -------------------------------------------------------------------------------------------------------------------------------
    #PUNTO2
    def getCamminoOttimo(self):

        #cammino + lungo con score minore
        self._bestPath=[]
        self._bestScore=float("inf")
        parziale=[]

        for nodo in self._nodes:  #inizio senza escludere tutti i cammini che hanno solo un nodo
            print(f"Inizio da nodo: {nodo} con successori: {list(self._grafo.successors(nodo))}")
            parziale.append(nodo)
            self._ricorsione(parziale)
            parziale.pop()

        if not self._bestPath:
            print("Nessun cammino ammissibile trovato.")

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        #ammissibile? vincoli
        #migliore?
        #ATTENZIONE!! quando len(parziale)==1 ha score=0 che è il migliore in assoluto, quindi non considerare quel caso
        if len(parziale)>1 and len(parziale) >= len(self._bestPath):
            score = self.calcolaScore(parziale)
            if score < self._bestScore:
                print(f"Soluzione migliore trovata")
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)


        ultimo = parziale[-1]
        for succ in self._grafo.successors(ultimo):
            #vincoli
            if succ not in parziale and ultimo.Essential != succ.Essential:
                pesoAttuale = 0
                pesoNuovo = 0

                if len(parziale)==2:
                    pesoAttuale = 0
                    pesoNuovo = self._grafo[ultimo][succ]["weight"]
                if len(parziale)>2:
                    pesoAttuale = self._grafo[parziale[-2]][ultimo]["weight"]
                    pesoNuovo =  self._grafo[ultimo][succ]["weight"]

                if pesoAttuale <= pesoNuovo:
                    print(f"Ricorsione: {parziale}")
                    parziale.append(succ)
                    self._ricorsione(parziale)
                    parziale.pop()
                else:
                    continue
            else:
                continue

    # -------------------------------------------------------------------------------------------------------------------------------
    def calcolaScore(self, listaNodi):

        print(f"Called function calcolaScore")
        pesoTot=0
        for i in range(0, len(listaNodi)-1):
            pesoTot += self._grafo[listaNodi[i]][listaNodi[i+1]]['weight']
        return pesoTot
# -------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    m = Model()
    print( len(m.getIdMapGenes()) )
    m.buildGraph(3, 7)
    print( m.getDetailsGraph() )
    print( m.getInteraction())
    print( m.getMaxNodi())