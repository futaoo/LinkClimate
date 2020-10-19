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

def tripledefine_locationcategory(**jsondata):
    uri_locationcategory = URIRef(str_ca + 'locationcategory/' + jsondata['id'])
    set_triples = [
        (uri_locationcategory, ca_property.hasId, Literal(jsondata['id'])),
        (uri_locationcategory, ca_property.hasName, Literal(jsondata['name']))
    ]
    return set_triples



def tripledefine_location(locationcategoryid, **jsondata):
    uri_location = URIRef(str_ca + 'location/' + jsondata['id'])
    uri_locationcategory = URIRef(str_ca + 'locationcategory/' + locationcategoryid)
    set_triples = [
        (uri_location, ca_property.inCategoryOf, uri_locationcategory),
        (uri_location, ca_property.hasId, Literal(jsondata['id'])),
        (uri_location, ca_property.hasName, Literal(jsondata['name']))
    ]
    return set_triples

def tripledefine_station(locationid, **jsondata):
    uri_station = URIRef(str_ca + 'station/' + jsondata['id'])
    uri_location = URIRef(str_ca + 'location/' + locationid)
    if not jsondata['elevation']:
        jsondata['elevation'] = ''
    set_triples = [
        (uri_station, ca_property.isLocatedIn, uri_location),
        (uri_station, ca_property.hasId, Literal(jsondata['id'])),
        (uri_station, ca_property.hasName, Literal(jsondata['name'])),
        (uri_station, ca_property.hasLatitude, Literal(jsondata['latitude'], datatype=XSD.float)),
        (uri_station, ca_property.hasLongitude, Literal(jsondata['longitude'], datatype=XSD.float)),
        (uri_station, ca_property.hasElevation, Literal(jsondata['elevation'], datatype=XSD.float)),
        (uri_station, ca_property.hasElevationUnit, Literal(jsondata['elevationUnit']))
    ]
    return set_triples

def tripledefine_dataset(**jsondata):
    uri_dataset = URIRef(str_ca + 'dataset/' + jsondata['id'])
    set_triples = [
        (uri_dataset, ca_property.hasId, Literal(jsondata['id'])),
        (uri_dataset, ca_property.hasName, Literal(jsondata['name']))
    ]
    return set_triples


def tripledefine_datacategory(**jsondata):
    uri_datacategory = URIRef(str_ca + 'datacategory/'+ jsondata['id'])
    set_triples = [
        (uri_datacategory, ca_property.hasId, Literal(jsondata['id'])),
        (uri_datacategory, ca_property.hasName, Literal(jsondata['name']))
    ]
    return set_triples

def tripledefine_datatype(datacategoryid, **jsondata):
    uri_datatype = URIRef(str_ca + 'datatype/' + jsondata['id'])
    uri_datacategory = URIRef(str_ca + 'datacategory/'+ datacategoryid)
    set_triples = [
        (uri_datatype, ca_property.inCategoryOf, uri_datacategory),
        (uri_datatype, ca_property.hasId, Literal(jsondata['id'])),
        (uri_datatype, ca_property.hasName, Literal(jsondata['name']))
    ]
    return set_triples

def tripledefine_data(datasetid, stationid, **jsondata):
    uri_data = URIRef(str_ca + 'observation/' + '{}_{}_at_{}'.format(jsondata['datatype'], jsondata['station'], jsondata['date']))
    uri_dataset = URIRef(str_ca + 'dataset/' + datasetid)
    uri_station = URIRef(str_ca + 'station/' + stationid)
    uri_datatype = URIRef(str_ca + 'datatype/' + jsondata['datatype'])

    set_triples = [
        (uri_data, ca_property.asDataOf, uri_dataset),
        (uri_data, ca_property.isObservedBy, uri_station),
        (uri_data, ca_property.observedDataType, uri_datatype),
        (uri_data, ca_property.observedAtTime, Literal(jsondata['date'], datatype=XSD.date)),
        (uri_data, ca_property.observedValue, Literal(jsondata['value'], datatype=XSD.float)),
        (uri_data, ca_property.hasAttributeFlag, Literal(jsondata['attributes']))
    ]
    return set_triples










#fixed part of ontology

def fetch_loccateids(limit=1000):
    jsondata = base_request.requestfrom(endpoint='/locationcategories', limit=limit)
    loccateids = [loccateid for loccateid in \
        list(map(lambda rec: rec.get('id'), jsondata['results']))]
    return loccateids

def fetch_locationids(locationcategoryid, offset, limit=1000):
    jsondata = base_request.requestfrom(endpoint='/locations', locationcategoryid=locationcategoryid, offset=offset, limit=limit)
    locationids = [locationid for locationid in \
        list(map(lambda rec: rec.get('id'), jsondata['results']))]
    return locationids


def fix_triplecreate_loccate(limit=1000):
    jsondata= base_request.requestfrom(endpoint='/locationcategories', limit=limit)
    #print(jsondata['metadata'])
    with concurrent.futures.ThreadPoolExecutor() as executor:
        triple_groups = list(executor.map(lambda x: tripledefine_locationcategory(**x), jsondata['results']))

    triples = list(itertools.chain.from_iterable(triple_groups))
    return triples

def fix_triplecreate_loc(loccateid='CNTRY', limit=1000):
    jsondata = base_request.requestfrom(endpoint='/locations', locationcategoryid=loccateid, limit=limit)
    #print(jsondata['metadata'])
    with concurrent.futures.ThreadPoolExecutor() as executor:
        triple_groups = list(executor.map(lambda x: tripledefine_location(locationcategoryid=loccateid, **x), jsondata['results']))

    triples = list(itertools.chain.from_iterable(triple_groups))
    return triples

def fix_triplecreate_datacate(limit=1000):
    jsondata = base_request.requestfrom(endpoint='/datacategories', limit=limit)
    #print(jsondata['metadata'])
    with concurrent.futures.ThreadPoolExecutor() as executor:
         triple_groups = list(executor.map(lambda x: tripledefine_datacategory(**x), jsondata['results']))

    triples = list(itertools.chain.from_iterable(triple_groups))

    return triples

def fetch_datactgrids(limit=1000):
    jsondata = base_request.requestfrom(endpoint='/datacategories', limit=limit)
    #print(jsondata['metadata'])
    datacategoryids = [datacategoryid for datacategoryid in \
        list(map(lambda rec: rec.get('id'), jsondata['results']))]
    return datacategoryids

def fetch_triplecreate_datatype(datacategoryids,limit=1000):
    triple_groups = []
    for datacategoryid in datacategoryids:
        triple_groups.append(triplecreate_datatype(datacategoryid=datacategoryid))
    triples = list(itertools.chain.from_iterable(triple_groups))
    return triples

def fix_triplecreate_station(locationid='FIPS:UK', limit=1000):
    jsondata = base_request.requestfrom(endpoint='/stations', locationid=locationid, limit=limit)
    #print(jsondata['metadata'])
    with concurrent.futures.ThreadPoolExecutor() as executor:
         triple_groups = list(executor.map(lambda x: tripledefine_station(locationid=locationid, **x), jsondata['results']))

    triples = list(itertools.chain.from_iterable(triple_groups))

    return triples


def fetch_stationids_by_loc(locationid, limit=1000):
    jsondata = base_request.requestfrom(endpoint='/stations', locationid=locationid, limit=limit)
    stationids = [stationid for stationid in \
        list(map(lambda rec: rec.get('id'), jsondata['results']))]
    return stationids

def fetch_triplecreate_data(datasetid, startdate, enddate, stationids, limit=1000):
    triple_groups = []
    for stationid in stationids:
        triple_groups.append(triplecreate_data(datasetid=datasetid, stationid=stationid, startdate=startdate, enddate=enddate, limit=limit))
    
    triples = list(itertools.chain.from_iterable(triple_groups))

    return triples





# vary from the change of parameters in functions
def triplecreate_datatype(datacategoryid, limit=1000):
    jsondata = base_request.requestfrom(endpoint='/datatypes', datacategoryid=datacategoryid, limit=limit)
    #print(jsondata['metadata'])
    with concurrent.futures.ThreadPoolExecutor() as executor:
         triple_groups = list(executor.map(lambda x: tripledefine_datatype(datacategoryid=datacategoryid,**x), jsondata['results']))

    triples = list(itertools.chain.from_iterable(triple_groups))

    return triples

def triplecreate_data(datasetid, stationid, startdate, enddate, limit=1000):
    jsondata = base_request.requestfrom(endpoint='/data', datasetid=datasetid, stationid=stationid, startdate=startdate, enddate=enddate, limit=limit)
    #print(jsondata['metadata'])
    with concurrent.futures.ThreadPoolExecutor() as executor:
         triple_groups = list(executor.map(lambda x: tripledefine_datatype(datasetid=datasetid, stationid=stationid, **x), jsondata['results']))

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



        
    


    





