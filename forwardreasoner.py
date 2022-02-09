
#goal: infer all hierarchy rules over the available statements in the ABox, 
# such that the queries can be answered.
from contextlib import AbstractContextManager
import copy 
from pydoc import doc
from rdflib import Graph, Literal, RDF, URIRef
import time



class ForwardReasoner:
    
    def print_rules(self):
        i = 0
        for (s,p,o) in self.aBox:
            i += 1
            print(i,": ",s,p,o+"\n")

    # Recursive Approach --------------------------------
    #def forwardTraverse (self, toVisit, toAddABox, step):

    #    step +=1 
    #    if toVisit == []:
    #        return
    #    for (sA,pA,oA) in self.aBox:
    #        for (sT,pT,oT) in toVisit:
    #            if( (sA,pA,oT) in self.aBox) == False:
    #                if( (sA,pA,oT) in toAddABox) == False:
    #                    toAddABox.append((sA, pA, oT))
    #            toVisit.remove( (sT,pT,oT))
    #            print("step: ", step, "list: ", toVisit, "\n")
    #            self.forwardTraverse(toVisit, toAddABox,step)
    #    return toAddABox

    # I can terminate when I ve done all inferences (when is that?)
    def forwardTraverse (self, toVisit, step):
        step +=1 
        if toVisit == []:
            return

        for (sA,pA,oA) in self.aBox:
            for (sT,pT,oT) in toVisit:

                if((sA,pA,oT) in self.aBox) == False:
                    self.aBox.append((sA, pA, oT))
                toVisit.remove((sT,pT,oT))
                print("step: ", step, "list: ", toVisit, "\n")
                self.forwardTraverse(toVisit, step)
        return


    #aBox [ 
    #        lightNovel a novel
    #     ]
    #tBox [ 
    #        light novel subclass novel
    #       novel subclass writtenwork
    #       writtenwork subclass creativework
    #     ]
    # I can terminate when:
    # lightNovel subClassOf Creative Work
    def forwardTraverseRecursive (self, toVisit, step, goal):
        #if toVisit == []:
        #    return
        if goal in self.aBox:
            return
        for (sA,pA,oA) in self.aBox:
            for (sT,pT,oT) in toVisit:
                if oA == sT:
                    if((sA,pA,oT) in self.aBox) == False:
                        self.aBox.append((sA, pA, oT))
                        #toVisit.remove((sT,pT,oT))
                        print("step: ", step, "list: ", toVisit, "\n")
                        step +=1 
                        self.forwardTraverseRecursive(toVisit, step, goal)             
        return
    #--------------------------------------------------------
    

    # Naive Approach ----------------------------------------
    def reason(self):
        while True:
            toAddABox = []
            #assuming pA is always :type
            #e.g. :lightNovel1 rdf:type :LightNovel .
            for (sA,pA,oA) in self.aBox:
                #i = 0 
                #assuming pA is always :subClassOf (we have on subclassof rules)
                for(sT,pT,oT) in self.tBox:
                    #i += 1
                    if oA == sT:
                        #print(str(i)) 
                        if( (sA,pA,oT) in self.aBox) == False:
                            toAddABox.append((sA, pA, oT))
            if toAddABox == []:
                break
            for (s,p,o) in toAddABox:
                self.aBox.append((s,p,o))
                #if toAdd == []:
                #    break
    #--------------------------------------------------------
    
    def execute_query(self,query):
        g = Graph()
        for t in self.aBox:
            g.add(t)
        for t in self.tBox:
            g.add(t)
        qres = g.query(query)

        return qres

    def __init__(self, abox, tbox):
        self.aBox = copy.copy(abox)
        self.tBox = copy.copy(tbox)
        print(self.aBox)
        print("initialize")
        f = open("resultsForwardChaining.txt", "w")

        start_time = time.time()
        self.reason() #Naive approach
        f.write("Naive Forward Chaining: %s \n"  % (time.time() - start_time))


        #toAddABox = self.forwardTraverse(tbox, [],0)
        #for (s,p,o) in toAddABox:
        #   self.aBox.append((s,p,o))
  

        goal =  (URIRef('http://www.dbpedia.org/lightNovel1'),URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),URIRef('http://www.dbpedia.org/CreativeWork'))
      
        # Naive approach

        print("self. abox", self.aBox)
        print("abox", abox)
        #reset boxes
        self.aBox = copy.copy(abox)
        self.tBox = copy.copy(tbox)
        print("abox after ", self.aBox)

        start_time = time.time()
        self.forwardTraverseRecursive(tbox, 0, goal)
        f.write("Recursive Forward Chaining: %s \n"  % (time.time() - start_time))


        

        self.print_rules()
        

    
    

