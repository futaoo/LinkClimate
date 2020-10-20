from dotmap import DotMap
from rdflib import URIRef, Literal
from rdflib.graph import Graph
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
from rdflib import Namespace
from dotmap import DotMap
import concurrent.futures
import itertools
import requests




class CANOAAV2:

    def __init__(self):
        self.prefix = DotMap()
        self.prefix.ca_class = Namespace('http://jresearch.ucd.ie/climate-kg/ca/class/')
        self.prefix.ca_property = Namespace('http://jresearch.ucd.ie/climate-kg/ca/property/')

        self.prefix_str = DotMap()
        self.prefix_str.resource_dataset = 'http://jresearch.ucd.ie/climate-kg/resource/dataset/'
        self.prefix_str.resource_datacategory = 'http://jresearch.ucd.ie/climate-kg/resource/datacategory/'
        self.prefix_str.resource_datatype = 'http://jresearch.ucd.ie/climate-kg/resource/datatype/'
        self.prefix_str.resource_locationcategory = 'http://jresearch.ucd.ie/climate-kg/resource/locationcategory/'
        self.prefix_str.resource_location = 'http://jresearch.ucd.ie/climate-kg/resource/location/'
        self.prefix_str.resource_station = 'http://jresearch.ucd.ie/climate-kg/resource/station/'
        self.prefix_str.resource_observation = 'http://jresearch.ucd.ie/climate-kg/resource/observation/'
        self.prefix_str.resource_result = 'http://jresearch.ucd.ie/climate-kg/resource/result/'

        self.graph = Graph()
        self.graph.bind('rdfs', RDFS)
        self.graph.bind('rdf', RDF)
        self.graph.bind('ca_class', self.prefix.ca_class)
        self.graph.bind('ca_property', self.prefix.ca_property)
        self.graph.bind('sosa', SOSA)


        self.classes = DotMap()
        tmp_class = self.prefix.ca_class
        self.classes.Dataset = tmp_class.Dataset
        self.classes.DataCategory = tmp_class.DataCategory
        self.classes.DataType = tmp_class.DataType
        self.classes.LocationCategory  = tmp_class.LocationCategory
        self.classes.Location = tmp_class.Location
        self.classes.Station = tmp_class.Station
        self.classes.Observation = tmp_class.Observation
        self.classes.Result = tmp_class.Result

        self.properties = DotMap()
        tmp_property = self.prefix.ca_property
        self.properties.hasUid = tmp_property.hasUid
        self.properties.hasId = tmp_property.hasId
        self.properties.hasName = tmp_property.hasName
        self.properties.isLocatedIn = tmp_property.isLocatedIn
        self.properties.hasElevation = tmp_property.hasElevation
        self.properties.hasElevationUnit = tmp_property.hasElevationUnit
        self.properties.hasLatitude = tmp_property.hasLatitude
        self.properties.hasLongitude = tmp_property.hasLongitude
        self.properties.inDataCategory = tmp_property.inDataCategory
        self.properties.inLocationCategory = tmp_property.inLocationCategory
        self.properties.recordedInDataset = tmp_property.recordedInDataset
        self.properties.recordedByStation = tmp_property.recordedByStation
        self.properties.recordedAsDataType = tmp_property.recordedAsDataType
        self.properties.resultTime = SOSA.resultTime
        self.properties.hasSimpleResult = SOSA.hasSimpleResult
        self.properties.hasAttributeFlag = tmp_property.hasAttributeFlag


        self.base_triples = DotMap()
        self.base_triples.classes = DotMap()
        self.base_triples.properties = DotMap()

        self.base_triples.classes.Dataset = [(self.classes.Dataset, RDF.type, RDFS.Class)]
        self.base_triples.classes.DataCategory = [(self.classes.DataCategory, RDF.type, RDFS.Class)]
        self.base_triples.classes.DataType = [(self.classes.DataType, RDF.type, RDFS.Class)]
        self.base_triples.classes.LocationCategory = [(self.classes.LocationCategory, RDF.type, RDFS.Class)]
        self.base_triples.classes.Location = [(self.classes.Location, RDF.type, RDFS.Class)]
        self.base_triples.classes.Station = [(self.classes.Station, RDF.type, RDFS.Class)]
        self.base_triples.classes.Observation = [(self.classes.Observation, RDFS.subClassOf, SOSA.Observation)]
        self.base_triples.classes.Result = [(self.classes.Result, RDFS.subClassOf, SOSA.Result)]

        self.base_triples.properties.hasUid = [
            (self.properties.hasUid, RDF.type, RDF.Property),
            (self.properties.hasUid, RDFS.range, RDFS.Literal),
            (self.properties.hasUid, RDFS.domain, self.classes.Dataset)
        ]
        self.base_triples.properties.hasId =[
            (self.properties.hasId, RDF.type, RDF.Property),
            (self.properties.hasId, RDFS.range, RDFS.Literal)
        ]
        self.base_triples.properties.hasName = [
            (self.properties.hasName, RDF.type, RDF.Property),
            (self.properties.hasName, RDFS.range, RDFS.Literal)
        ]
        self.base_triples.properties.isLocatedIn = [
            (self.properties.isLocatedIn, RDF.type, RDF.Property),
            (self.properties.isLocatedIn, RDFS.range, self.classes.Location),
            (self.properties.isLocatedIn, RDFS.domain, self.classes.Station)
        ]
        self.base_triples.properties.hasElevation = [
            (self.properties.hasElevation, RDF.type, RDF.Property),
            (self.properties.hasElevation, RDFS.range, RDFS.Literal),
            (self.properties.hasElevation, RDFS.domain, self.classes.Station)
        ]
        self.base_triples.properties.hasElevationUnit = [
            (self.properties.hasElevationUnit, RDF.type, RDF.Property),
            (self.properties.hasElevationUnit, RDFS.range, RDFS.Literal),
            (self.properties.hasElevationUnit, RDFS.domain, self.classes.Station)
        ]
        self.base_triples.properties.hasLatitude = [
            (self.properties.hasLatitude, RDF.type, RDF.Property),
            (self.properties.hasLatitude, RDFS.range, RDFS.Literal),
            (self.properties.hasLatitude, RDFS.domain, self.classes.Station)
        ]
        self.base_triples.properties.hasLongitude = [
            (self.properties.hasLongitude, RDF.type, RDF.Property),
            (self.properties.hasLongitude, RDFS.range, RDFS.Literal),
            (self.properties.hasLongitude, RDFS.domain, self.classes.Station)
        ]
        self.base_triples.properties.inDataCategory = [
            (self.properties.inDataCategory, RDF.type, RDF.Property),
            (self.properties.inDataCategory, RDFS.range, self.classes.DataCategory),
            (self.properties.inDataCategory, RDFS.domain, self.classes.DataType)
        ]
        self.base_triples.properties.inLocationCategory = [
            (self.properties.inLocationCategory, RDF.type, RDF.Property),
            (self.properties.inLocationCategory, RDFS.range, self.classes.LocationCategory),
            (self.properties.inLocationCategory, RDFS.domain, self.classes.Location)
        ]
        self.base_triples.properties.recordedInDataset = [
            (self.properties.recordedInDataset, RDF.type, RDF.Property),
            (self.properties.recordedInDataset, RDFS.range, self.classes.Dataset),
            (self.properties.recordedInDataset, RDFS.domain, self.classes.Result)
        ]
        self.base_triples.properties.recordedByStation = [
            (self.properties.recordedByStation, RDF.type, RDF.Property),
            (self.properties.recordedByStation, RDFS.range, self.classes.Station),
            (self.properties.recordedByStation, RDFS.domain, self.classes.Result)
        ]
        self.base_triples.properties.recordedAsDataType = [
            (self.properties.recordedAsDataType, RDF.type, RDF.Property),
            (self.properties.recordedAsDataType, RDFS.range, self.classes.DataType),
            (self.properties.recordedAsDataType, RDFS.domain, self.classes.Result)
        ]
        self.base_triples.properties.hasAttributeFlag = [
            (self.properties.hasAttributeFlag, RDF.type, RDF.Property),
            (self.properties.hasAttributeFlag, RDFS.range, RDFS.Literal),
            (self.properties.hasAttributeFlag, RDFS.domain, self.classes.Result)
        ]

        self.map_to_triples = dict()
        self.map_to_triples['locctgr'] = self.map_to_triples_locctgr
        self.map_to_triples['location'] = self.map_to_triples_location
        self.map_to_triples['station'] = self.map_to_triples_station
        self.map_to_triples['dataset'] = self.map_to_triples_dataset
        self.map_to_triples['datactgr'] = self.map_to_triples_datactgr
        self.map_to_triples['datatype'] = self.map_to_triples_datatype
        self.map_to_triples['data'] = self.map_to_triples_data



    def map_to_triples_locctgr(self, **jsondata):
        uri_locationcategory = URIRef(self.prefix_str.resource_locationcategory + jsondata['id'])
        triples = [
            (uri_locationcategory, RDF.type, self.classes.LocationCategory),
            (uri_locationcategory, self.properties.hasId, Literal(jsondata['id'])),
            (uri_locationcategory, self.properties.hasName, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_location(self, locationcategoryid, **jsondata):
        uri_location = URIRef(self.prefix_str.resource_location + jsondata['id'])
        uri_locationcategory = URIRef(self.prefix_str.resource_locationcategory + locationcategoryid)
        triples = [
            (uri_location, RDF.type, self.classes.Location),
            (uri_location, self.properties.inLocationCategory, uri_locationcategory),
            (uri_location, self.properties.hasId, Literal(jsondata['id'])),
            (uri_location, self.properties.hasName, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_station(self, locationid, **jsondata):
        uri_station = URIRef(self.prefix_str.resource_station + jsondata['id'])
        uri_location = URIRef(self.prefix_str.resource_location + locationid)
        if not jsondata['elevation']:
            jsondata['elevation'] = ''
        triples = [
            (uri_station, RDF.type, self.classes.Station),
            (uri_station, self.properties.isLocatedIn, uri_location),
            (uri_station, self.properties.hasId, Literal(jsondata['id'])),
            (uri_station, self.properties.hasName, Literal(jsondata['name'])),
            (uri_station, self.properties.hasLatitude, Literal(jsondata['latitude'], datatype=XSD.float)),
            (uri_station, self.properties.hasLongitude, Literal(jsondata['longitude'], datatype=XSD.float)),
            (uri_station, self.properties.hasElevation, Literal(jsondata['elevation'], datatype=XSD.float)),
            (uri_station, self.properties.hasElevationUnit, Literal(jsondata['elevationUnit']))
        ]
        return triples

    def map_to_triples_dataset(self, **jsondata):
        uri_dataset = URIRef(self.prefix_str.resource_dataset + jsondata['id'])
        triples = [
            (uri_dataset, RDF.type, self.classes.Dataset),
            (uri_dataset, self.properties.hasId, Literal(jsondata['id'])),
            (uri_dataset, self.properties.hasName, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_datactgr(self, **jsondata):
        uri_datacategory = URIRef(self.prefix_str.resource_datacategory + jsondata['id'])
        triples = [
            (uri_datacategory, RDF.type, self.classes.DataCategory),
            (uri_datacategory, self.properties.hasId, Literal(jsondata['id'])),
            (uri_datacategory, self.properties.hasName, Literal(jsondata['name']))
        ]
        return triples
    
    def map_to_triples_datatype(self, datacategoryid, **jsondata):
        uri_datatype = URIRef(self.prefix_str.resource_datatype + jsondata['id'])
        uri_datacategory = URIRef(self.prefix_str.resource_datacategory + datacategoryid)
        triples = [
            (uri_datatype, RDF.type, self.classes.DataType),
            (uri_datatype, self.properties.inDataCategory, uri_datacategory),
            (uri_datatype, self.properties.hasId, Literal(jsondata['id'])),
            (uri_datatype, self.properties.hasName, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_data(self, datasetid, **jsondata):
        uri_observation = URIRef(self.prefix_str.resource_observation + '{}_{}_at_{}'.format(jsondata['datatype'], jsondata['station'], jsondata['date']))
        uri_dataset = URIRef(self.prefix_str.resource_dataset + datasetid)
        uri_station = URIRef(self.prefix_str.resource_station + jsondata['station'])
        uri_datatype = URIRef(self.prefix_str.resource_datatype + jsondata['datatype'])

        triples = [
            (uri_observation, self.properties.recordedInDataset, uri_dataset),
            (uri_observation, self.properties.recordedByStation, uri_station),
            (uri_observation, self.properties.recordedAsDataType, uri_datatype),
            (uri_observation, self.properties.resultTime, Literal(jsondata['date'], datatype=XSD.date)),
            (uri_observation, self.properties.hasSimpleResult, Literal(jsondata['value'], datatype=XSD.float)),
            (uri_observation, self.properties.hasAttributeFlag, Literal(jsondata['attributes']))
        ]
        return triples

    def create_triples_from_json(self, json_results, mapflag, **mapfunctionparas):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            triple_groups = list(executor.map(lambda x: self.map_to_triples[mapflag](**mapfunctionparas, **x), json_results))
        triples = list(itertools.chain.from_iterable(triple_groups))
        return triples
  


class CDOWeb:

    def __init__(self, base_url:str, token:str):
        self.base_url = base_url
        self.request_token = token

    def requestfrom(self, endpoint:str, **requestparas):
        token = self.request_token
        url = self.base_url + endpoint
        params = requestparas
        head = {'Token':token}
        r = requests.get(url=url, headers=head, params=params)
        data = r.json()
        # print(data['results'])
        return data






    