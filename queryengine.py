from rdflib import Graph


class QueryEngine:
    def __init__(self, abox, tbox):
        self.abox = abox
        self.tbox = tbox


    def execute_query(self,query):
        g = Graph()
        for t in self.abox:
            g.add(t)
        for t in self.tbox:
            g.add(t)
        qres = g.query(query)

        return qres