from rdflib.graph import Graph
from ontfunctions import fetch_datactgrids, fetch_locationids, fetch_loccateids, fetch_stationids_by_loc, fetch_triplecreate_data, fetch_triplecreate_datatype, fix_triplecreate_datacate, fix_triplecreate_loc, fix_triplecreate_loccate, fix_triplecreate_station

from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD

from rdflib import Namespace


def fetch_all_locationids(loccateids):
    locationids = []
    for loccateid in loccateids:
        locationids += fetch_locationids(locationcategoryid=loccateid, offset=1)
        #locationids += fetch_locationids(locationcategoryid=loccateid, offset=1001)
        #locationids.append(fetch_locationids(locationcategoryid=loccateid, offset=2001))
    return locationids

def fetch_all_loccateids():
    loccateids = fetch_loccateids()
    return loccateids
        


def triples_ca_fix(loccateids, locationids, datacategoryids):

    triples_loccate = fix_triplecreate_loccate()

    triples_loc=[]
    for loccateid in loccateids:
        triples_loc += fix_triplecreate_loc(loccateid=loccateid)


    triples_station = []
    for locationid in locationids:
        triples_station += fix_triplecreate_station(locationid=locationid)

    triples_datacate = fix_triplecreate_datacate()
    triples_datatype = fetch_triplecreate_datatype(datacategoryids=datacategoryids)

    triples = triples_loccate + triples_station + triples_loc +triples_datacate + triples_datatype
    
    return triples


if __name__ == "__main__":

    # locationid = 'FIPS:UK'
    # loccateid = 'CNTRY'
    # stationids = fetch_stationids_by_loc(locationid=locationid)
    datacategoryids = fetch_datactgrids()
    loccateids = ['CITY']
    locationids = fetch_all_locationids(loccateids=loccateids)[1:3]
    #locationids = ['FIPS:UK']
    # print(locationids)

    triples = triples_ca_fix(locationids=locationids, loccateids=loccateids, datacategoryids=datacategoryids)
    
    
    
    #predefined prefixes
    wgs84 = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
    qudt = Namespace("http://qudt.org/1.1/schema/qudt#")
    unit = Namespace("http://qudt.org/1.1/vocab/unit#")
    dul = Namespace("http://www.loa-cnr.it/ontologies/DUL.owl#")
    ca = Namespace("http://jresearch.ucd.ie/ont/ca/resource/")
    cf =  Namespace("http://www.met.reading.ac.uk/~jonathan/CF_metadata/14.1/#")

    #basepreix string to be concatenated
    ca_class= Namespace("http://jresearch.ucd.ie/ont/ca/resource/class/")
    ca_property= Namespace("http://jresearch.ucd.ie/ont/ca/resource/property/")

    #used in fuctions that need to join some variables as the whole name of the URI
    str_ca = "http://jresearch.ucd.ie/ont/ca/resource/"

    #Initialize the base request
    
    g = Graph()
    g.bind("wgs84", wgs84)
    g.bind("qudt", qudt)
    g.bind("dul", dul)
    g.bind("cf", cf)
    g.bind("unit",unit)
    g.bind("ca_resource", ca)
    g.bind("ca_property", ca_property)
    g.bind("ca_class",ca_class)
    g.bind("ssn", SSN)
    g.bind("sosa", SOSA)
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
        

    for triple in triples:
        g.add(triple)

    print(g.serialize(format="turtle").decode("utf-8"))





