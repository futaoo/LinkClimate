import requests

# Fetch all available datasets
# https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets



#endpoint urls: 
# https://www.ncdc.noaa.gov/cdo-web/api/v2/{endpoint}
# where endpoint should be filled with the following entry points:
e_datasets = "/datasets"                      #A dataset is the primary grouping for data at NCDC.
e_datacategories = "/datacategories"          #A data category is a general type of data used to group similar data types.
e_datatypes = "/datatypes"                    #A data type is a specific type of data that is often unique to a dataset.
e_locationcategories = "/locationcategories"  #A location category is a grouping of similar locations.
e_locations = "/locations"                    #A location is a geopolitical entity.
e_stations = "/stations"                      #A station is a any weather observing platform where data is recorded.
e_data = "/data"                              #A datum is an observed value along with any ancillary attributes at a specific place and time.

base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2"

#auth token required from NOAA after the confirmation of email address
token = "dSPQHTPvpQGQvrlBvaCaxwbFjLSFANlC"
head = {'Token': token}

# Daily summary datasets of UK and Ireland

#1. Find the locationid of UK and Ireland 
#UK='FIPS:UK'    Ireland = 'FIPS:EI'
# Make sure the daily summary datasetid
#datasetid='GHCND'

# url_loc = base_url + e_locations
# params_loc = {"locationcategoryid":"CNTRY", "limit":1000}
# r_loc= requests.get(url=url_loc, headers=head, params=params_loc)
# data_loc = r_loc.json()
# print(data_loc)


# url_datasets = base_url + e_datasets
# limit = 1
# params = {"limit":limit, "datasetid":"GHCND"}

# # PARAMS = {"token":token}

# r = requests.get(url = url_datasets, headers=head, params=params)

# data = r.json()

# print(data)


url_data =  base_url + e_data
datasetid = 'GHCND'
locationid = ['FIPS:UK','FIPS:EI']
startdate = '2012-01-01'
enddate = '2012-01-02'
params = {
'datasetid':datasetid,
'locationid':locationid,
'startdate':startdate, 'enddate':enddate}
r = requests.get(url=url_data, headers=head, params=params)
data = r.json()
print(data)
