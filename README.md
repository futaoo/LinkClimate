# Link Climate: An Interoperable Knowledge Graph Platform for Climate Data
With the spirit of reproducible research, this repository includes a complete collection of codes required to generate the results and the diagrams presented in the paper:

> J. Wu, F. Orlandi, D. O'Sullivan, S. Dev, Link Climate: An Interoperable Knowledge Graph Platform for Climate Data, *Under Review*.

## Introduction to the Code Usage
This repository cantains the implementation of workflow components described in the paper, namely, defining the **Climate Analysis (CA)** ontology, fetching NOAA Climate Data Online (CDO), mapping CDO data to RDF data, saving RDF data to our triplestore and the task scheduler implementation doing the aboved jobs periodically.

The Python code implementation for the KG workflow is primarily stored in folder `autocdo`. Specifically,
- `autocdo/ca-ontology.py` contains the main reusable classes needed for creating the KG workflow:
  - **Class** `CANOAAV2` is the CA ontology class which neccessarily defines a set of semantic asertions that will be used in the knowledge model, and provides the essential functions which take NOAA CDO APIs as input to be mapped to RDF data.
  - **Class** `CDOWEB` is to configure the HTTP request to NOAA CDO APIs.
  - **Class** `OSM` is used to configure the HTTP request to OpenStreetMap APIs. To run this more stably, we set up **HTTPAdapter sessions** allowing to retry the requests without loss of responses when failures occur due to frequent requests.
- `autocdo/api-createtriples.py` reuse the class modules in  `autocdo/ca-ontology.py` so as to create the knowledge graph by following the steps : 1) fetching NOAA CDO data, 2) mapping CDO data to RDF data, 3) saving RDF data to our triplestore and 4) the task scheduler implementation doing the aboved jobs periodically.

## Understanding the output data
We provided some pieces of serialized RDF files in `output` with a supplementary instructions to faciliate the better comprehension on the workflow.
- `output/NOAA-sample.ttl` is a RDF triple file in turtle syntax chiefly using CA ontology to describe the NOAA climate observations.
- `output/ca-domain-range.ttl` is a sample set of ascertions that restrict the *subject* and *object* that can be associated with a specific *predicate* in a RDF triple statement.
- `output/station-address.ttl` is a sample RDF triple file that contains address information obtained from OpenStreetMap which is attached to the NOAA climate stations accordingly.
- `output/link-wikidata.ttl` showcases the geographical information linkage to Wikidata entities. Taking the following listing (taken from the file) as an example, `<http://jresearch.ucd.ie/climate-kg/resource/location/United_Kingdom_Oxford>` is enriched with `<http://jresearch.ucd.ie/climate-kg/resource/reference/tags_United_Kingdom_Oxford>` (mapped from OpenStreetMap) which is also linked to the wikidata entity `<http://www.wikidata.org/entity/Q34217>`.

```
@prefix ca_class: <http://jresearch.ucd.ie/climate-kg/ca/class/> .
@prefix ca_property: <http://jresearch.ucd.ie/climate-kg/ca/property/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://jresearch.ucd.ie/climate-kg/resource/location/United_Kingdom_Oxford> a ca_class:Location ;
    rdfs:label "city:United Kingdom_Oxford an instance of class Location" ;
    ca_property:referenceTags <http://jresearch.ucd.ie/climate-kg/resource/reference/tags_United_Kingdom_Oxford> .

<http://jresearch.ucd.ie/climate-kg/resource/reference/tags_United_Kingdom_Oxford> a ca_class:Reference ;
    rdfs:label "Reference:tags_United Kingdom_Oxford an instance of class Reference" ;
    ca_property:council_name "Oxford City Council" ;
    ca_property:council_style "city" ;
    ca_property:designation "non_metropolitan_district" ;
    ca_property:linked_place "city" ;
    ca_property:population "165000" ;
    ca_property:ref:gss "E07000178" ;
    ca_property:website "https://www.oxford.gov.uk/" ;
    ca_property:wikidata <http://www.wikidata.org/entity/Q34217> ;
```
