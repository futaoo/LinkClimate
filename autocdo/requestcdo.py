#requestcdo.py
import concurrent.futures
import requests


class Requestcdo:

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
#1.datacategories_GHCND_UK
#2.for every datacategories query datatype



def main(): 
    base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2"
    token = "dSPQHTPvpQGQvrlBvaCaxwbFjLSFANlC"
    requestcdo = Requestcdo(base_url=base_url,token=token)
    datacategories = requestcdo.requestfrom(endpoint="/stations", datasetid='GHCND', locationid='FIPS:UK')
    print(datacategories)

    # kwargs = [{'datacategoryid':datacategory} for datacategory in \
    #     list(map(lambda rec: rec.get('id'), datacategories))]


    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(lambda x: requestcdo.requestfrom(endpoint='/stations', datasetid='GHCND', locationid='FIPS:UK', **x), kwargs)


    

if __name__ == "__main__":
    main()


    

