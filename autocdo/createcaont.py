from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
from rdflib import Namespace
from rdflib import Graph

from requestcdo import Requestcdo

import concurrent.futures
import itertools

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
base_request = Requestcdo(base_url="https://www.ncdc.noaa.gov/cdo-web/api/v2",
token="dSPQHTPvpQGQvrlBvaCaxwbFjLSFANlC")


def describe_dataset():
    description = [
        (ca_class.Dataset, RDF.type, RDFS.Class),

        (ca_property.hasUid, RDF.type, RDF.Property),
        (ca_property.hasUid, RDFS.range, RDFS.Literal),

        (ca_property.hasMindate, RDF.type, RDF.Property),
        (ca_property.hasMindate, RDFS.range, RDFS.Literal),

        (ca_property.hasMaxdate, RDF.type, RDF.Property),
        (ca_property.hasMaxdate, RDFS.range, RDFS.Literal),

        (ca_property.hasName, RDF.type, RDF.Property),
        (ca_property.hasName, RDFS.range, RDFS.Literal),

        (ca_property.hasDatacoverage, RDF.type, RDF.Property),
        (ca_property.hasDatacoverage, RDFS.range, RDFS.Literal)
    ]
    return description

def describe_datacategories():
    description = [
        (ca_class.DataCategory, RDF.type, RDFS.Class),

        (ca_property.hasName, RDF.type, RDF.Property),
        (ca_property.hasName, RDFS.range, RDFS.Literal),

        (ca_property.hasId, RDF.type, RDF.Property),
        (ca_property.hasId, RDFS.range, RDFS.Literal)

    ]
    return description

def describe_datatypes():
    description = [
        (ca_class.DataType, RDF.type, RDFS.Class),

        (ca_property.hasId, RDF.type, RDF.Property),
        (ca_property.hasId, RDFS.range, RDFS.Literal),

        (ca_property.hasMindate, RDF.type, RDF.Property),
        (ca_property.hasMindate, RDFS.range, RDFS.Literal),

        (ca_property.hasMaxdate, RDF.type, RDF.Property),
        (ca_property.hasMaxdate, RDFS.range, RDFS.Literal),

        (ca_property.hasName, RDF.type, RDF.Property),
        (ca_property.hasName, RDFS.range, RDFS.Literal),

        (ca_property.hasDatacoverage, RDF.type, RDF.Property),
        (ca_property.hasDatacoverage, RDFS.range, RDFS.Literal)

    ]
    return description

def describe_locationcategories():
    description = [
        (ca_class.LocationCategory, RDF.type, RDFS.Class),

        (ca_property.hasName, RDF.type, RDF.Property),
        (ca_property.hasName, RDFS.range, RDFS.Literal),

        (ca_property.hasId, RDF.type, RDF.Property),
        (ca_property.hasId, RDFS.range, RDFS.Literal)
    ]
    return description

def describe_locations():
    description = [
        (ca_class.Location, RDF.type, RDFS.Class),

        (ca_property.hasId, RDF.type, RDF.Property),
        (ca_property.hasId, RDFS.range, RDFS.Literal),

        (ca_property.hasMindate, RDF.type, RDF.Property),
        (ca_property.hasMindate, RDFS.range, RDFS.Literal),

        (ca_property.hasMaxdate, RDF.type, RDF.Property),
        (ca_property.hasMaxdate, RDFS.range, RDFS.Literal),

        (ca_property.hasName, RDF.type, RDF.Property),
        (ca_property.hasName, RDFS.range, RDFS.Literal),

        (ca_property.hasDatacoverage, RDF.type, RDF.Property),
        (ca_property.hasDatacoverage, RDFS.range, RDFS.Literal)

    ]
    return description

def describe_stations():
    description = [
        (ca_class.Station, RDF.type, RDFS.Class),

        (ca_property.hasId, RDF.type, RDF.Property),
        (ca_property.hasId, RDFS.range, RDFS.Literal),

        (ca_property.hasMindate, RDF.type, RDF.Property),
        (ca_property.hasMindate, RDFS.range, RDFS.Literal),

        (ca_property.hasMaxdate, RDF.type, RDF.Property),
        (ca_property.hasMaxdate, RDFS.range, RDFS.Literal),

        (ca_property.hasName, RDF.type, RDF.Property),
        (ca_property.hasName, RDFS.range, RDFS.Literal),

        (ca_property.hasDatacoverage, RDF.type, RDF.Property),
        (ca_property.hasDatacoverage, RDFS.range, RDFS.Literal),

        (ca_property.hasElevation, RDF.type, RDF.Property),
        (ca_property.hasElevation, RDFS.range, RDFS.Literal),

        (ca_property.hasLatitude, RDF.type, RDF.Property),
        (ca_property.hasLatitude, RDFS.range, RDFS.Literal),

        (ca_property.hasLongitude, RDF.type, RDF.Property),
        (ca_property.hasLongitude, RDFS.range, RDFS.Literal),

        (ca_property.hasElevationUnit, RDF.type, RDF.Property),
        (ca_property.hasElevationUnit, RDFS.range, RDFS.Literal)
    ]
    return description

def tripledefine_station(**kwargs):
    uri_station = URIRef(str_ca + 'station/'+ kwargs['id'])
    set_striples = [
        (uri_station, ca_property.hasId, Literal(kwargs['id'])),
        (uri_station, ca_property.hasName, Literal(kwargs['name'])),
        (uri_station, ca_property.hasLatitude, Literal(kwargs['latitude'], datatype=XSD.float)),
        (uri_station, ca_property.hasLongitude, Literal(kwargs['longitude'], datatype=XSD.float)),
        (uri_station, ca_property.hasElevation, Literal(kwargs['elevation'], datatype=XSD.float)),
        (uri_station, ca_property.hasElevationUnit, Literal(kwargs['elevationUnit']))
    ]
    return set_striples


def tripledefine_datacategory(**kwargs):
    uri_datacategory = URIRef(str_ca + 'datacategory/'+ kwargs['id'])
    set_triples = [
        (uri_datacategory, ca_property.hasId, Literal(kwargs['id'])),
        (uri_datacategory, ca_property.hasName, Literal(kwargs['name']))
    ]
    return set_triples






def triplecreate_station(datasetid, locationid, limit=1000):
    
    # json_dataset = base_request.requestfrom(endpoint='/datasets' + '/' + datasetid, limit=limit)
    # uri_dataset = URIRef(str_ca + 'dataset/' + datasetid)
    # set_triples = [
    #     (uri_dataset, ca_property.hasId, Literal(json_dataset['id'])),
    #     (uri_dataset, ca_property.hasName, Literal(json_dataset['name']))
    #     ]
    json = base_request.requestfrom(endpoint='/stations', datasetid=datasetid,locationid=locationid, limit=limit)['results']

    with concurrent.futures.ThreadPoolExecutor() as executor:
         triple_groups = list(executor.map(lambda x: tripledefine_station(**x), json))

    triples = list(itertools.chain.from_iterable(triple_groups))

    return triples

def triplecreate_datacategory(datasetid, locationid, limit=1000):

    json = base_request.requestfrom(endpoint='/datacategories', datasetid=datasetid,locationid=locationid, limit=limit)['results']

    with concurrent.futures.ThreadPoolExecutor() as executor:
         triple_groups = list(executor.map(lambda x: tripledefine_datacategory(**x), json))

    triples = list(itertools.chain.from_iterable(triple_groups))

    return triples



    


   
    
    
    

# a = describe_locations()+describe_stations()
# g = Graph()
# g.bind("wgs84", wgs84)
# g.bind("qudt", qudt)
# g.bind("dul", dul)
# g.bind("cf", cf)
# g.bind("unit",unit)
# g.bind("ca", ca)
# g.bind("ssn", SSN)
# g.bind("sosa", SOSA)
# g.bind("rdfs", RDFS)
# g.bind("rdf", RDF)
    

# for triple in a:
#     g.add(triple)

# print(g.serialize(format="turtle").decode("utf-8"))



        
    


    





