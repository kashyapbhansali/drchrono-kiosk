from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
import views as drchrono_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^setup_kiosk/$', drchrono_views.setup_kiosk, name='setup_kiosk'),

    url(r'^office/(?P<office_id>[0-9]+)/$', drchrono_views.office, name='office'),

    url(r'^checkin/?(?P<message>[a-z]+)?/?$', drchrono_views.checkin, name='checkin'),

    url(r'^checkin/$', drchrono_views.checkin, name='checkin'),

    url(r'^demographics/$', drchrono_views.demographics, name='demographics'),

    url(r'^doctor/$', drchrono_views.doctor, name='doctor'),

    url(r'^mark_complete/(?P<apt_id>[0-9]+)/$', drchrono_views.mark_complete, name='mark_complete'),

    url(r'^callin/(?P<apt_id>[0-9]+)/$', drchrono_views.call_in, name='callin'),

    url(r'^logout/$', drchrono_views.logout, name='logout'),

    # url(r'^home/$', drchrono_views.home, name='home'),
    #
    # url(r'^user/$', drchrono_views.user, name='user'),
]
