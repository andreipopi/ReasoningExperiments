#-- to visualise the rdflib graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
#--
from rdflib import Graph
from rdflib.namespace import RDF, RDFS

from forwardreasoner import ForwardReasoner
from queryengine import QueryEngine
from backwardreasoner import BackwardReasoner

def load_data(path):
    g = Graph()
    g.parse(path)
    return g

def extract_abox_and_tbox(graph):
    abox = []
    tbox = []
    for (s,p,o) in graph:
        if p == RDFS.subClassOf:
            tbox.append((s,p,o)) 
        if p == RDF.type and o != RDFS.Class:
            abox.append((s,p,o))
    return abox, tbox

#extracts simplified boxes for visualisation purposes
def extract_simplified_abox_and_tbox(graphSimpl):
    simpl_abox = []
    simpl_tbox = []
    for (s,p,o) in graphSimpl:
        if p == RDFS.subClassOf:
            simpl_tbox.append((s.n3(graphSimpl.namespace_manager),p.n3(graphSimpl.namespace_manager),o.n3(graphSimpl.namespace_manager)))
        if p == RDF.type and o != RDFS.Class:
            simpl_abox.append((s.n3(graphSimpl.namespace_manager),p.n3(graphSimpl.namespace_manager),o.n3(graphSimpl.namespace_manager)))
    return simpl_abox, simpl_tbox

def print_results(qres):
    for row in qres:
        print(row)


if __name__ == '__main__':
    # load the ontology from file
    rdf_graph = load_data('data/ontology.ttl')
    
    #extract abox and tbox
    abox, tbox = extract_abox_and_tbox(rdf_graph)
    
    #simpl_abox, simpl_tbox = extract_simplified_abox_and_tbox(rdf_graph)
    #print(tbox)
    #print(simpl_tbox)
    #print("RDF graph",rdf_graph)
    #parsedGraph = rdflib_to_networkx_multidigraph(simpl_tbox)
    #pos = nx.spring_layout(parsedGraph, scale=2)
    #edge_labels = nx.get_edge_attributes(parsedGraph, 'r')
    #nx.draw_networkx_edge_labels(parsedGraph, pos, edge_labels=edge_labels)
    #nx.draw(parsedGraph, with_labels=True)
    #if not in interactive mode for 
    #plt.show()  


    # use a query engine or reasoner to answer the queries
    #reasoner = QueryEngine(abox, tbox)
    # once the ForwardReasoner is implemented you can uncomment this line and the second query should provide the same
    # answer as the first query

    #reasoner = ForwardReasoner(abox,tbox)

    # once the BackwardReasoner is implemented you can uncomment this line and the second query should provide the same
    # answer as the first query

    reasoner = BackwardReasoner(abox,tbox)

    # The first query simply looks for all LightNovels (which does not require reasoning)
    query1 = '''
    SELECT ?novel
        WHERE {
            ?novel a <http://www.dbpedia.org/LightNovel>.
        }
    '''
    # we print the results
    #print("results of the first query")
    #print_results(qres)

    # The second query looks for all CreativeWorks (which does require reasoning)
    query2 = '''
    SELECT ?work
        WHERE {
            ?work a <http://www.dbpedia.org/CreativeWork>.
        }
    '''
    # execute the query through the provided functionality of the QueryEngine
    qres = reasoner.execute_query(query2)
    
    # we print the results
    print("results of second query")
    print_results(qres)

