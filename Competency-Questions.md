Competency Questions (CQs)

- Where are all the sensors situated in a particular administrative region?
    
    <aside>
    💡 **Q1:** select out the sensors in the city
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+ca-p%3A+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2Fca%2Fproperty%2F%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0A%0ASELECT+%3Faddress+%3Fcity+%3Fcounty+WHERE+%7B+%0A++%3Cresource%2Fstation%2FGHCND%3AEI000003953%3E++ca-p%3AhasAddress++%3Faddress+.%0A++OPTIONAL+%7B%3Faddress+ca-p%3Acity+%3Fcity+.%7D%0A++OPTIONAL+%7B%3Faddress+ca-p%3Acounty+%3Fcounty+.%7D%0A%7D%0A%0A+++++++++++++++++++++++%0A+)
    
    construct:
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+ca-p%3A+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2Fca%2Fproperty%2F%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0A%0A%23CONSTRUCT+%3Faddress+%3Fcity+%3Fcounty+%0ACONSTRUCT+%7B+%0A++%3Cresource%2Fstation%2FGHCND%3AEI000003953%3E++ca-p%3AhasAddress++%3Faddress+.%0A++%3Faddress+ca-p%3Acity+%3Fcity+.%0A++%3Faddress+ca-p%3Acounty+%3Fcounty+.%0A%7D+%0A%0AWHERE+%7B+%0A++%3Cresource%2Fstation%2FGHCND%3AEI000003953%3E++ca-p%3AhasAddress++%3Faddress+.%0A++OPTIONAL+%7B%3Faddress+ca-p%3Acity+%3Fcity+.%7D%0A++OPTIONAL+%7B%3Faddress+ca-p%3Acounty+%3Fcounty+.%7D%0A%7D%0A%0A+++++++++++++++++++++++%0A+)
    
    **Additional answer**: address details can be queried and viewed from lod-view:
    
    [](http://jresearch.ucd.ie/climate-kg/resource/address/GHCND:EI000003953)
    
    </aside>
    

- Which sensor is the nearest to a certain sensor?
    
    <aside>
    💡 **Q1:** select the coordinates of the sensor
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+w3geo%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E%0A%0A%0A%0ASELECT+%3Flat+%3Flong+WHERE+%7B+%0A++%3Cresource%2Fstation%2FGHCND%3AEI000003953%3E++w3geo%3Alat+%3Flat%3B%0A++++++++++++++++++++++++++++++++++++++++w3geo%3Along+%3Flong+.%0A%7D%0A%0A+++++++++++++++++++++++%0A+)
    
    **Q2:** select the lat/long pairs for all of the sensors
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+w3geo%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E%0A%0A%0A%0ASELECT+%3Fsensors+%3Flat+%3Flong+WHERE+%7B+%0A++%3Fsensors+w3geo%3Alat+%3Flat%3B%0A+++++++++++w3geo%3Along+%3Flong+.++++++++++++++++++++++++++++++++++++%0A%7D%0A%0A+++++++++++++++++++++++%0A+)
    
    **Additional answer:** The nearest sensor can be calculated based on Q2 and Q1.
    
    </aside>
    
     
    
- What sensors are accessible within a given area of interest?
    
    <aside>
    💡 **Q1:** select the lat/long pairs for all of the sensors
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+w3geo%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E%0A%0A%0A%0ASELECT+%3Fsensors+%3Flat+%3Flong+WHERE+%7B+%0A++%3Fsensors+w3geo%3Alat+%3Flat%3B%0A+++++++++++w3geo%3Along+%3Flong+.++++++++++++++++++++++++++++++++++++%0A%7D%0A%0A+++++++++++++++++++++++%0A+)
    
    **Additional answer:** For geographical data representation, LinkClimate knowledge graph already includes a lat/long coordinate system which can be queried using Q1 likewise query. Locate accessible sensors within a specified region of interest by interacting with the GeoSPARQL engine, which automatically generates the results behind declarative queries.
    
    </aside>
    

- How can I group sensors according to a particular observed climatic variable?
    
    <aside>
    💡 **Q1**: SPARQL query that retrieves the sensors having precipitation results
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+w3geo%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0ASELECT+DISTINCT+%3Fsensor+WHERE+%7B+%0A++%3Fobs+%3Cca%2Fproperty%2FsourceStation%3E+%3Fsensor+%3B%0A+++++++sosa%3AhasResult%2F%3Cca%2Fproperty%2FwithDataType%3E+%3Cresource%2Fdatatype%2FPRCP%3E+.%0A%7D%0A+++++++++++++++++++++++%0A+)
    
    </aside>
    

- How to find climate variables that are recorded by a particular sensor?
    
    <aside>
    💡 **Q1**: find all climate variables monitored by a particular sensor
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+w3geo%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0ASELECT+DISTINCT+%3Fclimate_variable+WHERE+%7B+%0A++%3Fobs+%3Cca%2Fproperty%2FsourceStation%3E+%3Cresource%2Fstation%2FGHCND%3AEI000003969%3E+%3B%0A+++++++sosa%3AhasResult%2F%3Cca%2Fproperty%2FwithDataType%3E+%3Fclimate_variable%0A%7D%0A+++++++++++++++++++++++%0A+)
    
    </aside>
    

- How long has a certain climatic variable been monitored by a particular sensor?
    
    <aside>
    💡 **Q1:** find a increased order of sequence of dates on which precipitation is recorded for a given sensor
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0ASELECT+DISTINCT+%3Fdate+WHERE+%7B+%0A++%3Fobs+%3Cca%2Fproperty%2FsourceStation%3E+%3Cresource%2Fstation%2FGHCND%3AEI000003969%3E+%3B%0A+++++++sosa%3AresultTime+%3Fdate+%3B%0A+++++++sosa%3AhasResult%2F%3Cca%2Fproperty%2FwithDataType%3E+%3Cresource%2Fdatatype%2FPRCP%3E+.%0A%7D%0A+++++++++++++++++++++++%0A+)
    
    **Additional answer**: the whole recording duration of the climate variable can be calculated by deducting the oldest date from newest date in the sequence
    
    </aside>
    

- How can a time series for a single climatic variable be retrieved?
    
    <aside>
    💡 **Q1**: Time series created for average temperature.
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0ASELECT+%3Fvalue+%3Fdate+WHERE+%7B+%0A++%3Fobs+%3Cca%2Fproperty%2FsourceStation%3E+%3Cresource%2Fstation%2FGHCND%3AEI000003969%3E+%3B%0A+++++++sosa%3AhasSimpleResult+%3Fvalue%3B%0A+++++++sosa%3AresultTime+%3Fdate+%3B%0A++%09+++sosa%3AhasResult%2F%3Cca%2Fproperty%2FwithDataType%3E+%3Cresource%2Fdatatype%2FTAVG%3E+.%0A%7D%0A%0ALIMIT+400%0A+++++++++++++++++++++++%0A+)
    
    </aside>
    

- How can a time series for a number of different climatic variables be retrieved?
    
    <aside>
    💡 **Q1**: Time series for average temperature and precipitation monitored by a sensor
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0ASELECT+%3Fprcp+%3Ftavg+%3Fdate+WHERE+%7B+%0A++%3Fobs_t+%3Cca%2Fproperty%2FsourceStation%3E+%3Cresource%2Fstation%2FGHCND%3AEI000003969%3E+%3B%0A+++++++sosa%3AhasSimpleResult+%3Ftavg%3B%0A+++++++sosa%3AresultTime+%3Fdate+%3B%0A++%09+++sosa%3AhasResult%2F%3Cca%2Fproperty%2FwithDataType%3E+%3Cresource%2Fdatatype%2FTAVG%3E+.%0A++%7B%0A++++SELECT+%3Fprcp+%3Fdate+WHERE+%7B%0A++++++%3Fobs_p+%3Cca%2Fproperty%2FsourceStation%3E+%3Cresource%2Fstation%2FGHCND%3AEI000003969%3E+%3B%0A+++++++++++++sosa%3AhasSimpleResult+%3Fprcp%3B%0A+++++++%09+++++sosa%3AresultTime+%3Fdate+%3B%0A++%09+++++++++sosa%3AhasResult%2F%3Cca%2Fproperty%2FwithDataType%3E+%3Cresource%2Fdatatype%2FPRCP%3E+.++++++++++++%0A++++%7DLIMIT+400%0A++%7D%0A%7DLIMIT+400%0A+++++++++++++++++++++++%0A+)
    
    </aside>
    

- How can sensor observations be aggregated according to their temporal resolution? (from daily to monthly)
    
    <aside>
    💡 **Q1**:  Temperature aggregated on the basis of month during 2019 for a sensor
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+sosa%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E%0A%0ASELECT+(AVG(%3Fval)+as+%3Favg_val)+%3Fmonth+WHERE+%7B+%0A++%3Fobs+%3Cca%2Fproperty%2FsourceStation%3E+%3Cresource%2Fstation%2FGHCND%3AEI000003969%3E+%3B%0A+++++++sosa%3AhasSimpleResult+%3Fval%3B%0A+++++++sosa%3AresultTime+%3Fdate+%3B%0A++%09+++sosa%3AhasResult%2F%3Cca%2Fproperty%2FwithDataType%3E+%3Cresource%2Fdatatype%2FTAVG%3E+.%0A++BIND+(MONTH(%3Fdate)+AS+%3Fmonth)%0A++FILTER+(YEAR(%3Fdate)%3D2019)%0A++%0A%7D%0AGROUP+BY+%3Fmonth%0A+++++++++++++++++++++++%0A+)
    
    </aside>
    

- How can I determine the sensor's or station's geographical context?
    
    <aside>
    💡 **Q1**: find the address of a particular sensor
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+ca-p%3A+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2Fca%2Fproperty%2F%3E%0A%0A%0ASELECT+%3Faddress+WHERE+%7B+%0A++%3Cresource%2Fstation%2FGHCND%3AEI000003953%3E++ca-p%3AhasAddress++%3Faddress+.%0A%7D%0A%0A+++++++++++++++++++++++%0A+)
    
    </aside>
    

- How to include extra environmental data into a sensor's or set of sensors' knowledge graph in order to do cross-domain data analysis?
    
    <aside>
    💡 Q1: Access the water body information from Wikidata knowledge graph for a station/sensor
    
    [Apache Jena Fuseki - inspect dataset](http://jresearch.ucd.ie/kg/dataset.html?tab=query&ds=/climate#query=BASE+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2F%3E%0APREFIX+ca_property%3A+%3Chttp%3A%2F%2Fjresearch.ucd.ie%2Fclimate-kg%2Fca%2Fproperty%2F%3E%0APREFIX+wdt%3A+%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2F%3E%0A%0ASELECT+%3Fsta+%3Fwb%0AWHERE%7B%0A++%3Fsta+a+%3Cca%2Fclass%2FStation%3E+%3B%0A+++++++ca_property%3AhasAddress+%3Faddr+.%0A++%3Faddr+ca_property%3Acounty+%7C+ca_property%3Acity+%3Floc+.%0A++%3Floc+ca_property%3AreferenceTags%2Fca_property%3Awikidata+%3Fwd+.%0A++SERVICE+%3Chttps%3A%2F%2Fquery.wikidata.org%2Fsparql%3E+%7B%0A++%3Fwd+wdt%3AP206+%3Fwb+.%0A++%7D%0A%7D%0A%0A+++++++++++++++++++++++%0A+)
    
    </aside>
    

---

References

[FoodKG: A Semantics-Driven Knowledge Graph for Food Recommendation](https://paperpile.com/shared/d4uHzX)

[Methodology for ontology design and construction](http://www.scielo.org.mx/scielo.php?pid=S0186-10422019000500015&script=sci_arttext)
