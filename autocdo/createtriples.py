import datetime
import time
from ontology import CANOAAV2, CDOWeb
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from requests_toolbelt.multipart import encoder
import os
from utils import n_week_before, split_date_by_month


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

def fetch_all_data(r:CDOWeb, endpoint, limit=1000, **params):
    jsondata = r.requestfrom(**params, endpoint=endpoint, limit=limit)
    data = jsondata['results']

    result_num = jsondata['metadata']['resultset']['count']
    iterate_num = (result_num-1)//limit
    if iterate_num >= 1:
        i = 1
        while i <= iterate_num:
            iter_jsondata = r.requestfrom(**params, endpoint=endpoint, limit=limit, offset=i*limit+1) 
            data += iter_jsondata['results']
            i += 1
    return data



def find_cityids_of_country(r:CDOWeb, c_lable):
    all_locids = fetch_ids(r=r, endpoint='/locations', locationcategoryid = 'CITY')
    all_locids_by_c = []
    for id in all_locids:
        if id[5:7] == c_lable:
            all_locids_by_c.append(id)
    return all_locids_by_c



def create_triples(o:CANOAAV2, mapflag, r:CDOWeb, endpoint, mapfunctionparas = {}, **r_params):

    try:
        jsondata = fetch_all_data(r=r, endpoint=endpoint, **r_params)
        #jsondata = r.requestfrom(**r_params, endpoint=endpoint, limit=limit)['results']
        triples = o.create_triples_from_json(json_results=jsondata, mapflag=mapflag, **mapfunctionparas)
        return triples
    except Exception as e:
        print(e.__class__, "occurred.")

    # print(jsondata)



def upload_fix():
    o = CANOAAV2()
    rCDO = CDOWeb('https://www.ncdc.noaa.gov/cdo-web/api/v2', 'dSPQHTPvpQGQvrlBvaCaxwbFjLSFANlC')
    triples_locctgr = create_triples(o=o, mapflag='locctgr', r=rCDO, endpoint='/locationcategories')

    triples_loc_cntry = create_triples(o=o, mapflag='location', r=rCDO, endpoint='/locations', mapfunctionparas={'locationcategoryid':'CNTRY'},
    locationcategoryid = 'CNTRY')

    triples_station_cntry = []
    cntry_ids = ['FIPS:UK', 'FIPS:EI']
    for cntry_id in cntry_ids:
        triples_station_cntry += create_triples(o=o, mapflag='station', r=rCDO, endpoint='/stations', mapfunctionparas={'locationid':cntry_id}, locationid=cntry_id)

    triples_loc_city = create_triples(o=o, mapflag='location', r=rCDO, endpoint='/locations', mapfunctionparas={'locationcategoryid':'CITY'},
    locationcategoryid = 'CITY')

    triples_station_city = []
    c_lables = ['UK', 'EI']
    for c_label in c_lables:
        locationids = find_cityids_of_country(r=rCDO, c_lable=c_label)[1:3]
        for id in locationids:
            triples_station_city += create_triples(o=o, mapflag='station', r=rCDO, endpoint='/stations', mapfunctionparas={'locationid':id}, locationid=id)

    triples_datactgr = create_triples(o=o, mapflag='datactgr', r=rCDO, endpoint='/datacategories')

    triples_datatype = []
    datactgrids =  fetch_ids(r=rCDO, endpoint='/datacategories')
    for id in datactgrids:
        triples_datatype += create_triples(o=o, mapflag='datatype', r=rCDO, endpoint='/datatypes', mapfunctionparas={'datacategoryid':id}, datacategoryid=id)

    triples_ont = []
    base_triples_dict = o.base_triples.toDict()
    for key in base_triples_dict:
        for subkey in base_triples_dict[key]:
            triples_ont += base_triples_dict[key][subkey]

    triples_fix = triples_locctgr + triples_loc_city + triples_loc_cntry + triples_station_city + triples_station_cntry + triples_datactgr + triples_datatype + triples_ont

    ograph = o.graph
    for triple in triples_fix:
        ograph.add(triple)
    
    triple_file = ograph.serialize(format="turtle").decode("utf-8")
    with open('fixdata.ttl','w') as f:
        f.write(triple_file)
    multipart_data = encoder.MultipartEncoder(fields={'file': ('fixdata.ttl', open('fixdata.ttl', 'rb'), 'text/plain')})
    headers = {'Content-Type': multipart_data.content_type}
    requests.post('http://jresearch.ucd.ie/kg/climate/data', auth=('admin','KG@ucd.ie'), data=multipart_data, headers=headers)


def upload_data():
    print("%s: uploading triples now" % time.asctime())
    out_fmt = '%Y-%m-%d'
    date_of_today = datetime.datetime.today()
    date_before_n_week = n_week_before(n=4, date_of_today=date_of_today)
    time_intervals = split_date_by_month(begin=date_before_n_week.strftime(out_fmt), end=date_of_today.strftime(out_fmt))

    for time_interval in time_intervals:
        o = CANOAAV2()
        rCDO = CDOWeb('https://www.ncdc.noaa.gov/cdo-web/api/v2', 'dSPQHTPvpQGQvrlBvaCaxwbFjLSFANlC')
        locationids = ['FIPS:UK', 'FIPS:EI']
        triples_data = create_triples(o=o, mapflag='data', r=rCDO, endpoint='/data', mapfunctionparas={'datasetid':'GHCND'}, datasetid='GHCND',
        locationid=locationids, units='standard',startdate = time_interval['startdate'], enddate=time_interval['enddate'])

        ograph = o.graph
        for triple in triples_data:
            ograph.add(triple)
        triple_file = ograph.serialize(format="turtle").decode("utf-8")

        with open('data.ttl','w') as f:
            f.write(triple_file)
        multipart_data = encoder.MultipartEncoder(fields={'file': ('data.ttl', open('data.ttl', 'rb'), 'text/plain')})
        headers = {'Content-Type': multipart_data.content_type}
        requests.post('http://jresearch.ucd.ie/kg/climate/data', auth=('admin','KG@ucd.ie'), data=multipart_data, headers=headers)
        print('{} to {} : Upload Completed!!'.format(time_interval['startdate'], time_interval['enddate']))


# scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Shanghai'}, daemon=False)
# scheduler.add_job(upload_data, 'interval', weeks=1, start_date='2020-10-22 10:28:00', id='upload_triples')
# scheduler.start()
upload_fix()