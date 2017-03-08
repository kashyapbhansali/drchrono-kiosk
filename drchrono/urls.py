from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
import views as drchrono_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^setup_kiosk/$', drchrono_views.setup_kiosk, name='setup_kiosk'),

    url(r'^checkin/$', drchrono_views.checkin, name='checkin'),
    url(r'^demographics/$', drchrono_views.demographics, name='demographics'),

    url(r'^home/$', drchrono_views.home, name='home'),

    url(r'^user/$', drchrono_views.user, name='user'),

    url(r'^logout/$', drchrono_views.logout, name='logout'),

]
