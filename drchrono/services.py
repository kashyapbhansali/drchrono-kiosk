import requests
import datetime
from pprint import pprint as pp


def get_doctor_data(request):
    url = 'https://drchrono.com/api/users/current'
    r = requests.get(url, headers=request.session['headers'])
    r = r.json()
    return r


def get_offices(request):
    data_list = []
    url = 'https://drchrono.com/api/offices'
    r = requests.get(url, headers=request.session['headers'])
    print "get office request code:",r.status_code
    if r.status_code == 403:
        return data_list

    data_list.append(r.json())
    return data_list


def get_todays_appointments(request, appointment_data):
    #todo: filter appointments based on doctor_id, office_id
    url = 'https://drchrono.com/api/appointments'
    url = url + ''
    results = []
    while url:
        r = requests.get(url, headers=request.session['headers'])
        r = r.json()
        pp(r)
        for apt in r['results']:
            results.append(apt)

        url = r['next']

    #todo: save results to appointments model
    pass


def check_patient_appointment(request, appointment_data):
    patient_id = appointment_data['patient_id']
    date = appointment_data['date']
    url = 'https://drchrono.com/api/appointments'
    url = url + '?patient=' +str(patient_id) + '&date=' +date
    results = []
    while url:
        r = requests.get(url, headers=request.session['headers'])
        r = r.json()
        # print 'appt!!!!!:'
        # pp(r)
        for apt in r['results']:
            results.append(apt)

        url = r['next']

        if results:
            #result found
            return True

    return False


def check_get_demographics(request, checkin_data):
    fname = checkin_data['fname']
    lname = checkin_data['lname']
    ssn = checkin_data['ssn']
    url = 'https://drchrono.com/api/patients'
    url = url + '?first_name=' +fname +'&last_name=' +lname

    while url:
        r = requests.get(url, headers=request.session['headers'])
        r = r.json()
        pp(r)
        for patient in r['results']:
            if patient['first_name'] == fname and patient['last_name'] == lname and patient['social_security_number'] == ssn:
                return patient

        url = r['next']

    #no match
    return None