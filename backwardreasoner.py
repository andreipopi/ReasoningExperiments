from math import hypot
from typing import Union
from rdflib import Graph, Literal, RDF, URIRef
import time
import copy

class BackwardReasoner:

    def graphTraverseDFS (self,vertex, toVisit, visited):
        print("Vertex: ", vertex, "\n")
        
        if (vertex in visited) == False:
            visited.append(vertex)
        print("Visited: ", visited, "\n")
        toVisit = self.neighbours(vertex)
        #print("vertex",vertex)
        print("ToVisit: ", toVisit, "\n")
        if toVisit == []:
            return visited
        for v in toVisit:
            self.graphTraverseDFS(v, [], visited)
        return visited
     #return visited #returns when current vertex has no neighbours to visit

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
        toRemove = []
        #assuming pA is always :subClassOf
        #vertex: :CreativeWork
        #e.g. :WrittenWork rdf:subClassOf :CreativeWork .
        #print("TBOX size", len(self.tboxCopy))
        for (sT,pT,oT) in self.tboxCopy:
            if oT == vertex:
                neighbours.append(sT)
                #toRemove.append((sT,pT,oT))
                self.tboxCopy.remove((sT,pT,oT))
        #print("TBOX size", len(self.tboxCopy))
        #print(self.tboxCopy)
        return neighbours

    # This method demonstrates that when the neighbour() auxiliar method  is incorporated 
    # in the code, avoiding function call
    def recursiveBFSwithNeihbours (self, queue, visited):
        print(queue)
        if not queue: #if queue is empty, we are done poppping
            return #we return 
        current_v = queue.pop()
        neighbours = []
        #assuming pA is always :subClassOf
        #vertex: :CreativeWork
        #e.g. :WrittenWork rdf:subClassOf :CreativeWork .
        for (sT,pT,oT) in self.tboxCopy:
            if oT == current_v:
                neighbours.append(sT)
                self.tboxCopy.remove((sT,pT,oT))
        for n in neighbours:
             if (n in visited) == False:
                 visited.append(n)
                 print("visited", visited)
                 queue.append(n)
        self.graphTraverseBFS(queue, visited) #right before recursion stops, this returns and visited will contain all visited nodes                                  
        return  visited         #we finally return the list of all visited nodes, and recursion ends
                                #this return is only reached once, when the if not queue is trigerred and self.graphTraverseBFS is finally not going into a recursive call

    # End Recursive Approaches --------------------------------


    # Naive Approach ------------------------------------------
    # Returns a list of objects [URIRef("http://www.dbpedia.org/CreativeWork"), <http ://www. dbpedia . org/RadioProgram> ]
    def getQueryObjects(self):
        
        #initilize the list with the root element CreativeWork
        visited = [ URIRef("http://www.dbpedia.org/CreativeWork") ]
        # as long as no new objects can be added
        changed = True
        while changed:
            length = len(visited)
            for hypothesisObject in visited:
                # for each clause in the tBox
                # we assume that p is a subClassOf relation (thats how it was added)
                for (s,p,o) in self.tboxCopy:
                    if o == hypothesisObject:
                        #print(s, hypothesisObject)
                        self.tboxCopy.remove((s,p,o))
                        if (s in visited) == False:
                            visited = visited+[URIRef(s)]
                            #print("LIST:", hyphotesisObjectList)
            #print("lenght of list",len(hyphotesisObjectList))
            if len(visited) == length:
                changed = False
        return visited
    # End Naive Approach ----------------------------------------

    def execute_query(self,query2):
        # How queryObjects should look like: [rdflib.term.URIRef('http://www.dbpedia.org/CreativeWork'), rdflib.term.URIRef('http://www.dbpedia.org/WrittenWork'), rdflib.term.URIRef('http://www.dbpedia.org/Artwork'), rdflib.term.URIRef('http://www.dbpedia.org/Software'), rdflib.term.URIRef('http://www.dbpedia.org/Film'), rdflib.term.URIRef('http://www.dbpedia.org/RadioProgram'), rdflib.term.URIRef('http://www.dbpedia.org/Book'), rdflib.term.URIRef('http://www.dbpedia.org/Article'), rdflib.term.URIRef('http://www.dbpedia.org/Comic'), rdflib.term.URIRef('http://www.dbpedia.org/Annotation'), rdflib.term.URIRef('http://www.dbpedia.org/Painting'), rdflib.term.URIRef('http://www.dbpedia.org/Sculpture'), rdflib.term.URIRef('http://www.dbpedia.org/VideoGame'), rdflib.term.URIRef('http://www.dbpedia.org/Novel'), rdflib.term.URIRef('http://www.dbpedia.org/Manhua'), rdflib.term.URIRef('http://www.dbpedia.org/ComicStrip'), rdflib.term.URIRef('http://www.dbpedia.org/Manga'), rdflib.term.URIRef('http://www.dbpedia.org/Reference'), rdflib.term.URIRef('http://www.dbpedia.org/LightNovel')]
        # Naive approach

        f = open("results.txt", "w")

        #self.tboxCopy = copy.copy(self.tBox) #we will work on a copy of the tbox

        #start_time = time.time()
        #self.queryObjects = self.getQueryObjects()
        #runtime = time.time() - start_time
        #f.write("Naive Backward: %.9f \n"  % (runtime))

        # Recursive approach DFS
        self.tboxCopy = copy.copy(self.tBox) #reset the tbox copy
        start_time = time.time()
        self.queryObjects = self.graphTraverseDFS(URIRef("http://www.dbpedia.org/CreativeWork"), [], [])
        f.write("Recursive DFS Backward: %s \n"  % (time.time() - start_time))

        # Recursive approach DFS
        #self.tboxCopy = copy.copy(self.tBox) #reset the tbox copy
        # Recursive approach BFS
        #q = []
        #q.append(URIRef("http://www.dbpedia.org/CreativeWork"))
        #start_time = time.time()
        #self.queryObjects = self.graphTraverseBFS(q, [])
        #f.write("Recursive BFS Backward: %s \n"  % (time.time() - start_time))


        #print("objects", self.queryObjects)
        #query = self.build_and_execute_Query()
        f.close()
        return []
        #return self.g.query(query)


    def build_and_execute_Query(self):
        query = "SELECT ?work WHERE { "
        for elem in self.queryObjects:
            if elem != self.queryObjects[-1]:
                query = query + "{?work a <"+ elem+">.} UNION \n"
            else:
                query = query + "{?work a <"+ elem +">. } }"
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
        print("tBox saved", self.tBox)
        self.buildGraph()
        print("Graph created")
    
       