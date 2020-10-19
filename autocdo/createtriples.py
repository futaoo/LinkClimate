from ontology import CANOAAV2, CDOWeb


# def fetch_all_locctgrids(r:CDOWeb, limit=1000):
#     jsondata= r.requestfrom('/locationcategories', limit=limit)
#     ids = [id for id in list(map(lambda rec: rec.get('id'), jsondata['results']))]
#     return ids


# def fetch_locids_by_locctgrid(r:CDOWeb, locctgrid, limit=1000):
#     jsondata = r.requestfrom(endpoint='/locations', locationcategoryid=locctgrid, limit=limit)
#     ids = [id for id in list(map(lambda rec: rec.get('id'), jsondata['results']))]

#     result_num = jsondata['metadata']['resultset']['count']
#     iterate_num = (result_num-1)//limit

#     if iterate_num >= 1:
#         i = 1
#         while i <= iterate_num:
#             iter_jsondata = r.requestfrom(endpoint='/locations', locationcategoryid=locctgrid, limit=limit, offset=i*limit+1)
#             iter_ids = [iter_id for iter_id  in list(map(lambda rec: rec.get('id'), iter_jsondata['results']))]
#             ids += iter_ids
#             i += 1
#     return ids



def fetch_ids(r:CDOWeb, endpoint, limit=1000, **params):
    jsondata = r.requestfrom(**params, endpoint=endpoint, limit=limit)
    ids = [id for id in list(map(lambda rec: rec.get('id'), jsondata['results']))]

    result_num = jsondata['metadata']['resultset']['count']
    iterate_num = (result_num-1)//limit

    if iterate_num >= 1:
        i = 1
        while i <= iterate_num:
            iter_jsondata = r.requestfrom(**params, endpoint=endpoint, limit=limit, offset=i*limit+1)
            iter_ids = [iter_id for iter_id  in list(map(lambda rec: rec.get('id'), iter_jsondata['results']))]
            ids += iter_ids
            i += 1
    return ids


def find_cityids_of_country(c_lable):
    all_locids = fetch_ids(r=rCDO, endpoint='/locations', locationcategoryid = 'CITY')
    all_locids_by_c = []
    for id in all_locids:
        if id[5:7] == c_lable:
            all_locids_by_c.append(id)
    return all_locids_by_c



def create_triples(o:CANOAAV2, mapflag, r:CDOWeb, endpoint, mapfunctionparas = {}, limit=1000, **r_params):
    jsondata = r.requestfrom(**r_params, endpoint=endpoint, limit=limit)
    return o.create_triples_from_json(json_results=jsondata['results'], mapflag=mapflag, **mapfunctionparas)


o = CANOAAV2()
rCDO = CDOWeb('https://www.ncdc.noaa.gov/cdo-web/api/v2', 'dSPQHTPvpQGQvrlBvaCaxwbFjLSFANlC')

# triples_loccate = create_triples(o=o, mapflag='locctgr', r=rCDO, endpoint='/locationcategories')

# triples_loc = create_triples(o=o, mapflag='location', r=rCDO, endpoint='/locations', mapfunctionparas={'locationcategoryid':'CITY'},
# locationcategoryid = 'CITY')

# triples_station = []
# locationids = find_cityids_of_country(c_lable='UK')[1:3]
# for id in locationids:
#     triples_station += create_triples(o=o, mapflag='station', r=rCDO, endpoint='/stations', mapfunctionparas={'locationid':id}, locationid=id)

#triples_datactgr = create_triples(o=o, mapflag='datactgr', r=rCDO, endpoint='/datacategories')

datactgrids =  fetch_ids(r=rCDO, endpoint='/datacategories')
triples_datatype = []
for id in datactgrids:
    triples_datatype += create_triples(o=o, mapflag='datatype', r=rCDO, endpoint='/datatypes', mapfunctionparas={'datacategoryid':id}, datacategoryid=id)














    
    

# def triples_ca_fix(r:CDOWeb, loccateids, locationids, datacategoryids):



#     triples_loccate = fix_triplecreate_loccate()

#     triples_loc=[]
#     for loccateid in loccateids:
#         triples_loc += fix_triplecreate_loc(loccateid=loccateid)


#     triples_station = []
#     for locationid in locationids:
#         triples_station += fix_triplecreate_station(locationid=locationid)

#     triples_datacate = fix_triplecreate_datacate()
#     triples_datatype = fetch_triplecreate_datatype(datacategoryids=datacategoryids)

#     triples = triples_loccate + triples_station + triples_loc +triples_datacate + triples_datatype
    
#     return triples