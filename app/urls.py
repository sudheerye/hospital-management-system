from django.urls import include, re_path

from . import views

urlpatterns = [
    # auth
    re_path(r'^login/$', views.Login, name='login'),
    re_path(r'^register/$', views.Register, name='register'),
    re_path(r'^logout/$', views.Logout, name='logout'),
    
    # dashboard
    re_path(r'^dashboard/$', views.Dashboard, name='dashboard'),
    
    # roles
    re_path(r'^roles/$', views.Roles, name='roles'),
    re_path(r'^roles/create/$', views.CreateRole, name='create-role'),
    re_path(r'^roles/(?P<id>\d+)/$', views.EditRole, name='edit-role'),
    
    # doctors
    re_path(r'^doctors/$', views.Doctors, name='doctors'),
    re_path(r'^doctors/create/$', views.CreateDoctor, name='create-doctor'),
    re_path(r'^doctors/(?P<id>\d+)/$', views.EditDoctor, name='edit-doctor'),
    
    # doctors
    re_path(r'^staff/$', views.Staff, name='doctors'),
    re_path(r'^staff/create/$', views.CreateStaff, name='create-staff'),
    re_path(r'^staff/(?P<id>\d+)/$', views.EditStaff, name='edit-staff'),
    
    # patient
    re_path(r'^patient/$', views.Patient, name='patient'),
    re_path(r'^patient/create/$', views.CreatePatient, name='create-patient'),
    re_path(r'^patient/(?P<id>\d+)/$', views.EditPatient, name='edit-patient'),
    
    # appointments
    re_path(r'^appointments/$', views.Appointment, name='appointment'),
    re_path(r'^appointments/create/$', views.CreateAppointment, name='create-appointment'),
    re_path(r'^appointments/(?P<id>\d+)/prescription/$', views.Prescription, name='edit-appointment'),
    re_path(r'^appointments/(?P<id>\d+)/$', views.EditAppointment, name='edit-appointment'),
    
    
    # inventory
    re_path(r'^inventory/$', views.Inventory, name='inventory'),
    re_path(r'^inventory/create/$', views.CreateInventory, name='create-inventory'),
    re_path(r'^inventory/(?P<id>\d+)/$', views.EditInventory, name='edit-inventory'),
    
    # records
    re_path(r'^records/$', views.Records, name='records'),
    # re_path(r'^records/(?P<id>\d+)/$', views.EditRecords, name='edit-records'),
    
]