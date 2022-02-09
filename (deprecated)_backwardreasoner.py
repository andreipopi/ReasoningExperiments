from math import hypot
from typing import Union
from rdflib import Graph, Literal, RDF, URIRef
import time

class BackwardReasoner:
    # Recursive Approaches ------------------------------------
    # Step 0:
    # vertex: root vertex
    # toVisit: neighbours of root
    # visited: root

    def graphTraverseDFS (self,vertex, toVisit, visited):
        if (vertex in visited) == False:
            visited.append(vertex)
        print("vertex",vertex)
        if toVisit != []:
            toVisit = self.neighbours(vertex)
            for v in toVisit:
                self.graphTraverseDFS(v, self.neighbours(v), visited)
        return visited #returns when current vertex has no neighbours to visit
    
    def graphTraverseBFS (self, queue, visited):
        
        print(queue)
        if not queue: #if queue is empty, we are done poppping
            return #we return 
        current_v = queue.pop()
        for n in self.neighbours(current_v):
             if (n in visited) == False:
                 visited.append(n)
                 print("visited", visited)
                 queue.append(n)

        self.graphTraverseBFS(queue, visited) #right before recursion stops, this returns and visited will contain all visited nodes                                  
        return  visited         #we finally return the list of all visited nodes, and recursion ends
                                #this return is only reached once, when the if not queue is trigerred and self.graphTraverseBFS is finally not going into a recursive call

    def neighbours (self,vertex):
        neighbours = []
        #assuming pA is always :subClassOf
        #e.g. :LightNovel rdf:subClassOf :CreativeWork .
        for (sT,pT,oT) in self.tBox:
            if oT == vertex:
                neighbours.append(sT) 
        return neighbours
    # End Recursive Approaches --------------------------------


    # Naive Approach ------------------------------------------
    # Returns a list of objects [URIRef("http://www.dbpedia.org/CreativeWork"), <http ://www. dbpedia . org/RadioProgram> ]
    def getQueryObjects(self):
        #initilize the list with the root element CreativeWork
        hyphotesisObjectList = [ URIRef("http://www.dbpedia.org/CreativeWork") ]
        # assuming the p is always a subClassOf relation 
        # as long as no new objects can be added
        changed = True
        while changed:
            length = len(hyphotesisObjectList)
            for hypothesisObject in hyphotesisObjectList:
                # for each clause in the tBox
                # we assume that p is a subClassOf relation (thats how it was added)
                for (s,p,o) in self.tBox:
                    if o == hypothesisObject:
                        #print(s, hypothesisObject)
                        if (s in hyphotesisObjectList) == False:
                            hyphotesisObjectList = hyphotesisObjectList+[URIRef(s)]
                            #print("LIST:", hyphotesisObjectList)
            #print("lenght of list",len(hyphotesisObjectList))
            if len(hyphotesisObjectList) == length:
                changed = False
        return hyphotesisObjectList
    # End Naive Approach ----------------------------------------

    def execute_query(self,query2):
        # How queryObjects should look like: [rdflib.term.URIRef('http://www.dbpedia.org/CreativeWork'), rdflib.term.URIRef('http://www.dbpedia.org/WrittenWork'), rdflib.term.URIRef('http://www.dbpedia.org/Artwork'), rdflib.term.URIRef('http://www.dbpedia.org/Software'), rdflib.term.URIRef('http://www.dbpedia.org/Film'), rdflib.term.URIRef('http://www.dbpedia.org/RadioProgram'), rdflib.term.URIRef('http://www.dbpedia.org/Book'), rdflib.term.URIRef('http://www.dbpedia.org/Article'), rdflib.term.URIRef('http://www.dbpedia.org/Comic'), rdflib.term.URIRef('http://www.dbpedia.org/Annotation'), rdflib.term.URIRef('http://www.dbpedia.org/Painting'), rdflib.term.URIRef('http://www.dbpedia.org/Sculpture'), rdflib.term.URIRef('http://www.dbpedia.org/VideoGame'), rdflib.term.URIRef('http://www.dbpedia.org/Novel'), rdflib.term.URIRef('http://www.dbpedia.org/Manhua'), rdflib.term.URIRef('http://www.dbpedia.org/ComicStrip'), rdflib.term.URIRef('http://www.dbpedia.org/Manga'), rdflib.term.URIRef('http://www.dbpedia.org/Reference'), rdflib.term.URIRef('http://www.dbpedia.org/LightNovel')]

        # Naive approach
        f = open("results.txt", "w")
        start_time = time.time()
        self.queryObjects = self.getQueryObjects()
        f.write("Naive Backward: %s \n"  % (time.time() - start_time))

        

        # Recursive approach BFS
        q = []
        q.append(URIRef("http://www.dbpedia.org/CreativeWork"))
        start_time = time.time()
        self.queryObjects = self.graphTraverseBFS(q, [])
        f.write("Recursive BFS Backward: %s \n"  % (time.time() - start_time))


        # Recursive approach DFS
        start_time = time.time()
        self.queryObjects = self.graphTraverseDFS(URIRef("http://www.dbpedia.org/CreativeWork"), self.neighbours(URIRef("http://www.dbpedia.org/CreativeWork")), [URIRef("http://www.dbpedia.org/CreativeWork")])
        f.write("Recursive DFS Backward: %s \n"  % (time.time() - start_time))

        print("objects", self.queryObjects)

        query = self.build_and_execute_Query()
        #print("this is the query", query)
        f.close()
        
        return self.g.query(query)


    def build_and_execute_Query(self):
        query = "SELECT ?work WHERE { "
        for elem in self.queryObjects:
            if elem != self.queryObjects[-1]:
                query = query + "{?work a <"+ elem+">.} UNION \n"
            else:
                query = query + "{?work a <"+ elem +">. } }"
        #print("this is the query", query)
        return query

    def buildGraph (self):
        self.g = Graph()
        for t in self.aBox:
            self.g.add(t)
        for t in self.tBox:
            self.g.add(t)

    def print_rules(self):
        i = 0
        for (s,p,o) in self.aBox:
            i += 1
            print(i,": ",s,p,o+"\n")

    def __init__(self, abox, tbox):
        self.aBox = abox
        print("aBox saved")
        self.tBox = tbox
        print("tBox saved")
        self.buildGraph()
        print("Graph created")
    
       