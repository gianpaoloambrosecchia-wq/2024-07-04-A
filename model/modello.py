import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0


    def getPath(self):
        self._bestPath = []
        self._bestScore = 0
        parziale = []
        for n in self._graph.nodes:
            durata_corr = n.duration
            parziale.append(n)
            self._ricorsione(parziale, durata_corr)
            parziale.pop()
        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale, durata_prec):

        score = self._calcolaScore(parziale)
        if score > self._bestScore:
            self._bestScore = score
            self._bestPath = copy.deepcopy(parziale)

        for n in self._graph.successors(parziale[-1]):
            durata_corr = n.duration
            if durata_corr > durata_prec and n not in parziale:
                if self._verificaSolAmmissibile(parziale, n):
                    parziale.append(n)
                    self._ricorsione(parziale, durata_corr)
                    parziale.pop()


    def _verificaSolAmmissibile(self, parziale, n):
        c = 0
        mese = n.datetime.month
        for p in parziale:
            if p.datetime.month == mese:
                c+=1

        if c == 3:
            return False
        else:
            return True


    def _calcolaScore(self, parziale):
        score = 0
        for i in range(len(parziale)):
            if i == 0:
                score += 100
            else:
                if parziale[i].datetime.month == parziale[i-1].datetime.month:
                    score += 200
                else:
                    score += 100

        return score


    def buildGraph(self, year, shape):
        self._graph.clear()
        self._idMap = {}
        nodes = DAO.getAllNodes(year, shape)
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMap[node.id] = node

        self._addEdges(year, shape)


    def _addEdges(self, year, shape):
        edges = DAO.getAllEdges(year, shape, self._idMap)
        for edge in edges:
            if edge[0].datetime > edge[1].datetime:
                self._graph.add_edge(edge[1], edge[0])
            elif edge[0].datetime < edge[1].datetime:
                self._graph.add_edge(edge[0], edge[1])


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getCompConnDetails(self):
        numCC = nx.number_weakly_connected_components(self._graph)
        maxCC = max(nx.weakly_connected_components(self._graph), key=len)
        return numCC, maxCC

#
    def getAllYears(self):
        return DAO.getAllYears()


    def getShapesForYear(self, year):
        return DAO.getShapesForYear(year)

