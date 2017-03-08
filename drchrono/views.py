# Create your views here.
import datetime
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout as drchrono_logout
from django.core.mail import send_mail,send_mass_mail
from .models import PatientModel
from .forms import *
from django.conf import settings
from services import *
from pprint import pprint as pp


def setup_kiosk(request):
    #todo: get list of day's appointments and save to model at time of setup


    #check if authenticated
    if not request.user.is_authenticated():
        return redirect('/')
    #get user instance
    user_instance = request.user.social_auth.get(provider='drchrono')
    #saving data to session
    request.session['doctor_access_token'] =  user_instance.extra_data['access_token']
    request.session['headers'] = {
        'Authorization': 'Bearer %s' % request.session['doctor_access_token'],
    }

    results = get_offices(request)
    request.session['doctor_data'] = get_doctor_data(request)
    pp(results)

    context = {'doctor':request.session['doctor_data']}

    return render(request, 'setup_kiosk.html', context)


def checkin(request):
    checkin_form = CheckinForm(request.POST or None)
    context = {'form': checkin_form}
    #todo: query appoints data and validate the user

    #check if user data is valid
    if checkin_form.is_valid():
        fname = checkin_form.cleaned_data['fname']
        lname = checkin_form.cleaned_data['lname']
        ssn = checkin_form.cleaned_data['ssn']

        checkin_data = {
            'fname' : fname,
            'lname' : lname,
            'ssn' : ssn
        }
        #if form valid, go ahead and get patient info
        results = check_get_demographics(request, checkin_data)
        if not results:
            context['error_message'] = 'Your details seem to be incorrect.'
        else:
            #check if the appointment was scheduled
            output = check_patient_appointment(request, {'patient_id': results['id'], 'date': datetime.date.today().isoformat()})
            if output:
                request.session['patient_demographics'] = results
                return redirect('/demographics')
            else:
                context['error_message'] = 'No such appointment Scheduled.'

    return render(request, 'checkin.html', context)


def demographics(request):
    form = DemographicsForm(data = request.POST or None, initial=request.session['patient_demographics'])
    if form.is_valid():
        #todo: update demographics in model and call api
        #todo: mark the patient as arrived
        return redirect('/checkin')

    context = {'results': request.session['patient_demographics'], 'form': form}
    return render(request, 'demographics.html', context)


def home(request):
    if not request.user.is_authenticated():
        return redirect('/')

    template = 'home.html'
    context = {'username': request.user}
    user_instance = request.user.social_auth.get()
    #access_token = user_instance.extra_data['access_token']
    request.session['access_token'] =  user_instance.extra_data['access_token']
    access_token = request.session['access_token']
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    # this endpoint returns a few lists of patients at a time
    # it has next and previous points to indicate if more patients are available
    patients_url = 'https://drchrono.com/api/patients'
    patient_list = []

    while True:
        r = requests.get(patients_url, headers=headers)
        #print r.raise_for_status()
        patient_data = r.json()
        #pprint(patient_data)
        patient_list.extend(patient_data['results'])
        if not patient_data['next']:
            break

    #save data using PatientModel

    for patient in patient_list:
        #defuult date if birthdate not available
        dob = '0001-01-01'
        if patient['date_of_birth']:
            dob = patient['date_of_birth']
        p = PatientModel(
            first_name=patient['first_name'],
            last_name=patient['last_name'],
            doctor_id=patient['doctor'],
            gender=patient['gender'],
            birthday=dob,
            patient_id=patient['id'],
            patient_email=patient['email']
        )
        p.save()

    return render(request, template, context)

def user(request):
    #get all patients who have an email id and birthdate
    message = settings.EMAIL_BIRTHDAY_DEFAULT_MESSAGE
    p = PatientModel.objects.exclude(patient_email="")
    birthdays = PatientModel.objects.filter(birthday__day=datetime.date.today().day,birthday__month=datetime.date.today().month).exclude(birthday__year=1)
    birthday_email_list = map(lambda x:x['patient_email'],birthdays.values())
    #pprint(birthday_email_list)
    #pprint(birthdays)
    form = birthdayEmailForm(request.POST or None, initial={'message': message})
    confirmation = None

    if form.is_valid():
        name = "drchrono team"
        subject = "Happy Birthday from drchrono!"
        message = form.cleaned_data['message']
        from_email = "drchrono@drchrono.com"
        recipient_list = birthday_email_list
        #datatuple for sending mass mail
        email_tuple = ((subject, message, from_email, recipient_list),)
        count = send_mass_mail(email_tuple, fail_silently=False)
        confirmation = "Birthday wishes were sent to %s people." % count

    template = 'user.html'
    context = {'patient_data': p, 'form': form, 'confirmation': confirmation, 'birthdays': birthdays}


    return render(request, template, context)

def logout(request):
    drchrono_logout(request)
    return redirect('/')