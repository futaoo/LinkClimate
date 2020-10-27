from dotmap import DotMap
from rdflib import URIRef, Literal
from rdflib.graph import Graph
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SSN, TIME, \
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
        self.prefix.sosa = Namespace('http://www.w3.org/ns/sosa/')
        self.prefix.geo = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
        self.prefix.qudt = Namespace('http://qudt.org/1.1/schema/qudt#')

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
        self.graph.bind('sosa', self.prefix.sosa)
        self.graph.bind('geo', self.prefix.geo)
        self.graph.bind('qudt', self.prefix.qudt)


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
        self.properties.uid = tmp_property.uid
        self.properties.id = tmp_property.id
        self.properties.name = tmp_property.name
        self.properties.isLocatedIn = tmp_property.isLocatedIn
        self.properties.elev = self.prefix.geo.alt
        self.properties.elevUnit = tmp_property.altitudeMeasuredIn
        self.properties.lat = self.prefix.geo.lat
        self.properties.long = self.prefix.geo.long
        self.properties.inDataCategory = tmp_property.inDataCategory
        self.properties.inLocationCategory = tmp_property.inLocationCategory
        self.properties.recordedInDataset = tmp_property.recordedInDataset
        self.properties.sourceStation = tmp_property.sourceStation
        self.properties.withDataType = tmp_property.withDataType
        self.properties.resultTime = self.prefix.sosa.resultTime
        self.properties.hasSimpleResult = self.prefix.sosa.hasSimpleResult
        self.properties.hasResult = self.prefix.sosa.hasResult
        self.properties.attributeFlag = tmp_property.attributeFlag
        self.properties.numericValue = self.prefix.qudt.numericValue


        self.base_triples = DotMap()
        self.base_triples.classes = DotMap()
        self.base_triples.properties = DotMap()

        self.base_triples.classes.Dataset = [(self.classes.Dataset, RDF.type, RDFS.Class), (self.classes.Dataset, RDFS.label, Literal('Class Dataset'))]
        self.base_triples.classes.DataCategory = [(self.classes.DataCategory, RDF.type, RDFS.Class), (self.classes.DataCategory, RDFS.label, Literal('Class DataCategory'))]
        self.base_triples.classes.DataType = [(self.classes.DataType, RDF.type, RDFS.Class), (self.classes.DataType, RDFS.label, Literal('Class DataType'))]
        self.base_triples.classes.LocationCategory = [(self.classes.LocationCategory, RDF.type, RDFS.Class), (self.classes.LocationCategory, RDFS.label, Literal('Class LocationCategory'))]
        self.base_triples.classes.Location = [(self.classes.Location, RDF.type, RDFS.Class), (self.classes.Location, RDFS.label, Literal('Class Location'))]
        self.base_triples.classes.Station = [(self.classes.Station, RDF.type, RDFS.Class), (self.classes.Station, RDFS.label, Literal('Class Station'))]
        self.base_triples.classes.Observation = [(self.classes.Observation, RDFS.subClassOf, self.prefix.sosa.Observation), (self.classes.Observation, RDFS.label, Literal('Class Observation'))]
        self.base_triples.classes.Result = [(self.classes.Result, RDFS.subClassOf, self.prefix.sosa.Result), (self.classes.Result, RDFS.label, Literal('Class Result'))]

        self.base_triples.properties.uid = [
            (self.properties.uid, RDF.type, RDF.Property),
            (self.properties.uid, RDFS.range, RDFS.Literal),
            (self.properties.uid, RDFS.domain, self.classes.Dataset)
        ]
        self.base_triples.properties.id =[
            (self.properties.id, RDF.type, RDF.Property),
            (self.properties.id, RDFS.range, RDFS.Literal)
        ]
        self.base_triples.properties.name = [
            (self.properties.name, RDF.type, RDF.Property),
            (self.properties.name, RDFS.range, RDFS.Literal)
        ]
        self.base_triples.properties.isLocatedIn = [
            (self.properties.isLocatedIn, RDF.type, RDF.Property)
        ]
        self.base_triples.properties.elevUnit = [
            (self.properties.elevUnit, RDF.type, RDF.Property),
            (self.properties.elevUnit, RDFS.range, RDFS.Literal)
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
        self.base_triples.properties.sourceStation = [
            (self.properties.sourceStation, RDF.type, RDF.Property),
            (self.properties.sourceStation, RDFS.range, self.classes.Station),
            (self.properties.sourceStation, RDFS.domain, self.classes.Observation)
        ]
        self.base_triples.properties.withDataType = [
            (self.properties.withDataType, RDF.type, RDF.Property),
            (self.properties.withDataType, RDFS.range, self.classes.DataType),
            (self.properties.withDataType, RDFS.domain, self.classes.Result)
        ]
        self.base_triples.properties.attributeFlag = [
            (self.properties.attributeFlag, RDF.type, RDF.Property),
            (self.properties.attributeFlag, RDFS.range, RDFS.Literal),
            (self.properties.attributeFlag, RDFS.domain, self.classes.Result)
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
            (uri_locationcategory, RDFS.label, Literal('{}: an instance of class LocationCategory'.format(jsondata['name']))),
            (uri_locationcategory, self.properties.id, Literal(jsondata['id'])),
            (uri_locationcategory, self.properties.name, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_location(self, locationcategoryid, **jsondata):
        uri_location = URIRef(self.prefix_str.resource_location + jsondata['id'])
        uri_locationcategory = URIRef(self.prefix_str.resource_locationcategory + locationcategoryid)
        triples = [
            (uri_location, RDF.type, self.classes.Location),
            (uri_location, RDFS.label, Literal('{}: an instance of class Location'.format(jsondata['name']))),
            (uri_location, self.properties.inLocationCategory, uri_locationcategory),
            (uri_location, self.properties.id, Literal(jsondata['id'])),
            (uri_location, self.properties.name, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_station(self, locationid, **jsondata):
        uri_station = URIRef(self.prefix_str.resource_station + jsondata['id'])
        uri_location = URIRef(self.prefix_str.resource_location + locationid)
        if not jsondata['elevation']:
            jsondata['elevation'] = ''
        triples = [
            (uri_station, RDF.type, self.classes.Station),
            (uri_station, RDFS.label, Literal('{}: an instance of class Station'.format(jsondata['name']))),
            (uri_station, self.properties.isLocatedIn, uri_location),
            (uri_station, self.properties.id, Literal(jsondata['id'])),
            (uri_station, self.properties.name, Literal(jsondata['name'])),
            (uri_station, self.properties.lat, Literal(jsondata['latitude'], datatype=XSD.float)),
            (uri_station, self.properties.long, Literal(jsondata['longitude'], datatype=XSD.float)),
            (uri_station, self.properties.elev, Literal(jsondata['elevation'], datatype=XSD.float)),
            (uri_station, self.properties.elevUnit, Literal(jsondata['elevationUnit']))
        ]
        return triples

    def map_to_triples_dataset(self, **jsondata):
        uri_dataset = URIRef(self.prefix_str.resource_dataset + jsondata['id'])
        triples = [
            (uri_dataset, RDF.type, self.classes.Dataset),
            (uri_dataset, RDFS.label, Literal('{}: an instance of class Dataset'.format(jsondata['name']))),
            (uri_dataset, self.properties.id, Literal(jsondata['id'])),
            (uri_dataset, self.properties.name, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_datactgr(self, **jsondata):
        uri_datacategory = URIRef(self.prefix_str.resource_datacategory + jsondata['id'])
        triples = [
            (uri_datacategory, RDF.type, self.classes.DataCategory),
            (uri_datacategory, RDFS.label, Literal('{}: an instance of class DataCategory'.format(jsondata['name']))),
            (uri_datacategory, self.properties.id, Literal(jsondata['id'])),
            (uri_datacategory, self.properties.name, Literal(jsondata['name']))
        ]
        return triples
    
    def map_to_triples_datatype(self, datacategoryid, **jsondata):
        uri_datatype = URIRef(self.prefix_str.resource_datatype + jsondata['id'])
        uri_datacategory = URIRef(self.prefix_str.resource_datacategory + datacategoryid)
        triples = [
            (uri_datatype, RDF.type, self.classes.DataType),
            (uri_datatype, RDFS.label, Literal('{}: an instance of class DataType'.format(jsondata['name']))),
            (uri_datatype, self.properties.inDataCategory, uri_datacategory),
            (uri_datatype, self.properties.id, Literal(jsondata['id'])),
            (uri_datatype, self.properties.name, Literal(jsondata['name']))
        ]
        return triples

    def map_to_triples_data(self, datasetid, **jsondata):
        uri_observation = URIRef(self.prefix_str.resource_observation + '{}_{}_at_{}'.format(jsondata['datatype'], jsondata['station'], jsondata['date']))
        uri_result = URIRef(self.prefix_str.resource_result + '{}_{}_at_{}'.format(jsondata['datatype'], jsondata['station'], jsondata['date']))
        uri_dataset = URIRef(self.prefix_str.resource_dataset + datasetid)
        uri_station = URIRef(self.prefix_str.resource_station + jsondata['station'])
        uri_datatype = URIRef(self.prefix_str.resource_datatype + jsondata['datatype'])

        triples = [
            (uri_observation, RDF.type, self.classes.Observation),
            (uri_observation, RDFS.label, Literal('An obeservation to {} from station (id={}) made at {}'.format(jsondata['datatype'], jsondata['station'], jsondata['date']))),
            (uri_observation, self.properties.hasResult, uri_result),
            (uri_observation, self.properties.resultTime, Literal(jsondata['date'], datatype=XSD.date)),
            (uri_observation, self.properties.hasSimpleResult, Literal(jsondata['value'], datatype=XSD.float)),
            (uri_observation, self.properties.sourceStation, uri_station),
            (uri_result, RDF.type, self.classes.Result),
            (uri_result, RDFS.label, Literal('An observation result about {}'.format(jsondata['datatype']))),
            (uri_result, self.properties.recordedInDataset, uri_dataset),
            (uri_result, self.properties.withDataType, uri_datatype),
            (uri_result, self.properties.numericValue, Literal(jsondata['value'], datatype=XSD.float)),
            (uri_result, self.properties.attributeFlag, Literal(jsondata['attributes']))
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









    