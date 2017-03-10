import datetime
from pprint import pprint as pp

import requests


def get_doctor_data(request):
    url = 'https://drchrono.com/api/users/current'
    r = requests.get(url, headers=request.session['headers'])
    r = r.json()
    return r


def get_offices(request):
    data_list = []
    url = 'https://drchrono.com/api/offices'
    while url:
        r = requests.get(url, headers=request.session['headers'])
        r = r.json()

        for office in r['results']:
            data_list.append(office)

        url = r['next']

    return data_list


def load_todays_appointments(request):
    doctor = request.session['doctor_data']['id']
    office = request.session['office_data']['id']
    # pp(office)
    date = datetime.date.today().strftime('%Y-%m-%d')
    url = 'https://drchrono.com/api/appointments'
    url = url + '?doctor=' + str(doctor) + '&office=' + str(office) + '&date=' + str(date)
    results = []
    while url:
        r = requests.get(url, headers=request.session['headers'])
        r = r.json()
        for apt in r['results']:
            results.append(apt)
        url = r['next']

    return results


def check_patient_appointment(request, appointment_data):
    patient_id = appointment_data['patient_id']
    date = appointment_data['date']
    url = 'https://drchrono.com/api/appointments'
    url = url + '?patient=' + str(patient_id) + '&date=' + date
    results = []
    while url:
        r = requests.get(url, headers=request.session['headers'])
        r = r.json()
        for apt in r['results']:
            results.append(apt)

        url = r['next']

        if results:
            # result found
            return True

    return False


def check_get_demographics(request, checkin_data):
    fname = checkin_data['fname']
    lname = checkin_data['lname']
    ssn = checkin_data['ssn']
    url = 'https://drchrono.com/api/patients'
    url = url + '?first_name=' + fname + '&last_name=' + lname

    while url:
        r = requests.get(url, headers=request.session['headers'])
        r = r.json()
        # pp(r)
        for patient in r['results']:
            if patient['first_name'] == fname and patient['last_name'] == lname:
                if patient['social_security_number'] == ssn:
                    return patient

        url = r['next']

    # no match
    return None
