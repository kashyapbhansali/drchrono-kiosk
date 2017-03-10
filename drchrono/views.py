# Create your views here.
from pprint import pprint as pp

from django.conf import settings
from django.contrib.auth import logout as drchrono_logout
from django.core.mail import send_mass_mail
from django.shortcuts import render, redirect

from services import *
from .forms import *
from .models import PatientModel, AppointmentModel


def setup_kiosk(request):
    # check if authenticated
    if not request.user.is_authenticated():
        return redirect('/')
    # get user instance
    user_instance = request.user.social_auth.get(provider='drchrono')
    # saving data to session
    request.session['doctor_access_token'] = user_instance.extra_data['access_token']
    request.session['headers'] = {
        'Authorization': 'Bearer %s' % request.session['doctor_access_token'],
    }

    offices = get_offices(request)
    pp(offices)
    request.session['doctor_data'] = get_doctor_data(request)

    context = {'doctor': request.session['doctor_data'], 'offices': offices}
    return render(request, 'setup_kiosk.html', context)


def office(request, office_id):
    request.session['office_data'] = {'id': 0}
    request.session['office_data']['id'] = office_id

    # loading appointments based on office selection
    appointments = load_todays_appointments(request)
    for apt in appointments:
        a, created = AppointmentModel.objects.update_or_create(
            id=apt['id'],
            doctor=apt['doctor'],
            patient=apt['patient'],
            office=apt['office'],
            defaults={
                'exam_room': apt['exam_room'],
                'reason': apt['reason'],
                'status': apt['status'],
                'deleted_flag': apt['deleted_flag'],
                'scheduled_time': apt['scheduled_time'],
                # 'arrival_time': '0001-01-01',
                # 'call_in_time': '0001-01-01',
            },
        )
        if created:
            print 'New Patient Created!'
        else:
            print 'Patient Exists'
    return redirect('/checkin')


def checkin(request, message=''):
    checkin_form = CheckinForm(request.POST or None)
    context = {'form': checkin_form, 'message': message}

    # check if user data is valid
    if checkin_form.is_valid():
        fname = checkin_form.cleaned_data['fname']
        lname = checkin_form.cleaned_data['lname']
        ssn = checkin_form.cleaned_data['ssn']
        checkin_data = {'fname': fname, 'lname': lname, 'ssn': ssn}

        # if form valid, go ahead and get patient info
        results = check_get_demographics(request, checkin_data)
        if not results:
            context['error_message'] = 'Your details seem to be incorrect.'
        else:
            # check if the appointment was scheduled
            output = check_patient_appointment(request,
                                               {'patient_id': results['id'], 'date': datetime.date.today().isoformat()})
            if output:
                request.session['patient_demographics'] = results
                return redirect('/demographics')
            else:
                context['error_message'] = 'No such appointment Scheduled.'

    return render(request, 'checkin.html', context)


def demographics(request):
    form = DemographicsForm(data=request.POST or None,
                            initial=request.session['patient_demographics'])
    if form.is_valid():
        # todo: update patient demographics
        # todo: mark the patient as arrived and save timing info to model
        patient = form.cleaned_data['id']
        doctor = request.session['doctor_data']['id']
        office = request.session['office_data']['id']
        arrival_time = datetime.datetime.now()
        status = 'Arrived'
        # assuming patient has only one appointment scheduled in a day.
        # since not using appointment id to update appt status
        # todo: my logged in doctor id is different
        a = AppointmentModel.objects.filter(patient=patient, office=office).earliest('scheduled_time')
        # .update(arrival_time=arrival_time, status=status)
        a.arrival_time = arrival_time
        a.status = status
        a.save()

        print 'Patient %d, Doctor %d, status updated to arrived' % (patient, doctor)
        # pp(AppointmentModel.objects.all())
        return redirect('/checkin/updated')

    context = {'results': request.session['patient_demographics'], 'form': form}
    return render(request, 'demographics.html', context)


def doctor(request):
    # load todays appointments order by scheduled_time
    current_day = datetime.date.today().day
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    appts = AppointmentModel.objects.filter(scheduled_time__day=current_day,
                                            scheduled_time__month=current_month,
                                            scheduled_time__year=current_year).order_by('scheduled_time')
    pp(appts)

    # logic for calculating average time
    apt_for_avg_time = appts.filter(status='Completed')
    avg_time = 0
    count = 0
    sum = 0
    for a in apt_for_avg_time:
        count = count + 1
        time_diff = a.call_in_time - a.arrival_time
        sum = sum + time_diff.total_seconds()

    if count != 0:
        avg_time = (sum / 60) / count

    print datetime.datetime.now()
    context = {'appointments': appts, 'current_time': datetime.datetime.now(), 'avg_time': avg_time}
    return render(request, 'doctor.html', context)


def mark_complete(request, apt_id):
    # set patient-id's status to completed in appointment model
    AppointmentModel.objects.filter(id=apt_id).update(status='Complete')
    print 'apt %d , status set to In Session.'
    return redirect('/doctor')


def call_in(request, apt_id):
    # set patient-id's call in time and status to In Session in appointment model
    call_in_time = datetime.datetime.now().isoformat()
    AppointmentModel.objects.filter(id=apt_id).update(call_in_time=call_in_time, status='In Session')
    print 'apt %d , status set to In Session.'
    return redirect('/doctor')


def logout(request):
    # todo: before logout post today's appointments data using api
    # for development purpose : clear db on logout
    AppointmentModel.objects.all().delete()
    drchrono_logout(request)
    return redirect('/')
