import requests
import datetime
from pprint import pprint as pp
#get offices for doctor

def get_offices(url , headers):
    data_list = []
    r = requests.get(url, headers=headers)
    print "get office request code:",r.status_code
    if r.status_code == 403:
        return data_list

    data_list.append(r.json())
    return data_list


def get_demographics(url, headers, checkin_data):
    data_list = []
    fname = checkin_data['fname']
    lname = checkin_data['lname']
    ssn = checkin_data['ssn']
    url = url + '?first_name=' +fname +'&last_name=' +lname

    while url:
        r = requests.get(url, headers=headers)
        r = r.json()
        pp(r)
        for patient in r['results']:
            if patient['first_name'] == fname and patient['last_name'] == lname and patient['social_security_number'] == ssn:
                return patient

        url = r['next']

    #no match
    return None