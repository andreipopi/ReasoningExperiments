from rdflib import Graph
from rdflib.namespace import RDF, RDFS

from backwardreasoner import BackwardReasoner
from forwardreasoner import ForwardReasoner
from queryengine import QueryEngine


def load_data(path):
    g = Graph()
    g.parse(path)
    return g

def extract_abox_and_tbox(rdf_graph):
    abox = []
    tbox = []
    for (s,p,o) in rdf_graph:
        if p == RDFS.subClassOf:
            tbox.append((s,p,o))
        if p == RDF.type and o != RDFS.Class:
            abox.append((s,p,o))
    return abox, tbox

def print_results(qres):
    for row in qres:
        print(row)


if __name__ == '__main__':
    # load the ontology from file
    rdf_graph = load_data('data/ontology.ttl')
    # extract abox and tbox
    abox, tbox = extract_abox_and_tbox(rdf_graph)
    # use a query engine or reasoner to answer the queries
    reasoner = QueryEngine(abox, tbox)
    # once the ForwardReasoner is implemented you can uncomment this line and the second query should provide the same
    # answer as the first query

    #reasoner = ForwardReasoner(abox,tbox)

    # once the BackwardReasoner is implemented you can uncomment this line and the second query should provide the same
    # answer as the first query

    #reasoner = BackwardReasoner(abox,tbox)

    # The first query simply looks for all LightNovels (which does not require reasoning)
    query1 = '''
    SELECT ?novel
        WHERE {
            ?novel a <http://www.dbpedia.org/LightNovel>.
        }
    '''
    # execute the query through the provided functionality of the QueryEngine
    qres = reasoner.execute_query(query1)

    # we print the results
    print_results(qres)

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
    print_results(qres)

