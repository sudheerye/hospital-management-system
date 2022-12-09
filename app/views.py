from django.shortcuts import render
from django.shortcuts import redirect
from app import models
from six import ensure_binary
from hashlib import md5


# Create your views here.
def Login(request):
    if request.method == 'POST':
        user = models.User.objects.filter(email=request.POST['email'], password=request.POST['password'])
        if user:
            role = models.Role.objects.get(id=user[0].role_id)
            print(role.name)
            request.session['user'] = user[0].id
            request.session['role'] = role.name.lower()
            response = redirect('/a/dashboard/')
            return response
        else:
            response = redirect('/a/login/?status=0&msg=login-failed')
            return response      
        
    if request.method == 'GET':
        return render(request, 'login.html')

def Register(request):
    # register user and redirect to login page
    if request.method == 'POST':
        try:
            # get ADMIN role
            role = models.Role.objects.get(name='ADMIN')
            # create user
            user = models.User()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.password = request.POST['password']
            user.role = role
            user.save()
            response = redirect('/a/login/?status=1&msg=register-success')
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/register/?status=0&msg=register-failed')
            return response
    # render template
    elif request.method == 'GET':
        return render(request, 'register.html')
    
    
def Dashboard(request):
    # render dashboard
    try:
        if request.method == 'GET':
            total_patients = models.Patient.objects.all().count()
            total_appointments = models.Appointment.objects.all().count()
            total_active_appointments = models.Appointment.objects.filter(status='PENDING').count()
            total_completed_appointments = models.Appointment.objects.filter(status='COMPLETED').count()
            total_doctors = models.DoctorDetails.objects.all().count()
            total_inventory = models.Inventory.objects.all().count()
            total_health_records = models.HealthRecord.objects.all().count()
            context = {
                'patients': total_patients,
                'appointments': total_appointments,
                'active_appointments': total_active_appointments,
                'completed_appointments': total_completed_appointments,
                'doctors': total_doctors,
                'inventory': total_inventory,
                'health_records': total_health_records,
            }
            return render(request, 'dashboard.html', context)
        else:
            return render(request, 'dashboard.html')
    except Exception as e:
        response = redirect('/a/login/?status=0&msg=login-required')
        return response


def Logout(request):
    # logout user and redirect to login page
    if request.method == 'GET':
        try:
            del request.session['user']
            del request.session['role']
            response = redirect('/a/login/')
            return response
        except Exception as e:
            response = redirect('/a/dashboard/')
            return response
    


def Roles(request):
    if request.method == 'GET':
        roles = models.Role.objects.all()
        for role in roles:
            print(role.id)
        context = {
            "roles": roles
        }
        return render(request, 'roles.html', context)
    
def CreateRole(request):
    # render template
    if request.method == 'GET':
        return render(request, 'roles-create.html')
    # create role
    elif request.method == 'POST':
        try:
            # create role
            role = models.Role()
            role.name = request.POST['name']
            role.save()
            response = redirect('/a/roles/{0}/?status=1&msg=role-created'.format(role.id))
            return response
        except Exception as e:
            response = redirect('/a/roles/create/?status=0&msg=role-create-failed')
            return response    

def EditRole(request, id):
    if request.method == 'GET':
        role = models.Role.objects.get(id=id)
        context = {
            "id": role.id,
            "name": role.name
        }           
        return render(request, 'roles-edit.html', context)
    elif request.method == 'POST':
        try:
            role = models.Role.objects.get(id=id)
            role.name = request.POST['name']
            role.save()
            response = redirect('/a/roles/{0}/?status=1&msg=role-updated'.format(id))
            return response
        except Exception as e:
            response = redirect('/a/roles/{0}/?status=0&msg=failed'.format(id))
            return response
        
        
# Doctors

def Doctors(request):
    if request.method == 'GET':
        doctor_role = models.Role.objects.get(name='DOCTOR')
        # include doctor details model too
        doctors = models.User.objects.filter(role=doctor_role)
        for doctor in doctors:
            doctor.doctor_details = models.DoctorDetails.objects.get(doctor=doctor)
        context = {
            "doctors": doctors
        }
        return render(request, 'doctors.html', context)
        
        
def CreateDoctor(request):
    # render template
    if request.method == 'GET':
        return render(request, 'doctors-create.html')
    # create role
    elif request.method == 'POST':
        try:
            # get DOCTOR role
            role = models.Role.objects.get(name='DOCTOR')
            # create role
            doctor = models.User()
            doctor.first_name = request.POST['first_name']
            doctor.last_name = request.POST['last_name']
            doctor.email = request.POST['email']
            doctor.password = request.POST['password']
            doctor.role = role
            doctor.save()
            # doctor details
            doctor_details = models.DoctorDetails()
            doctor_details.doctor = doctor
            doctor_details.title = request.POST['title']
            doctor_details.gender = request.POST['gender']
            doctor_details.specialization = request.POST['specialization']
            doctor_details.department = request.POST['department']
            doctor_details.consultation_fee = request.POST['consultation_fee']
            doctor_details.phone_number = request.POST['phone_number']
            
            doctor_details.address_1 = request.POST['address_1']
            doctor_details.address_2 = request.POST['address_2']
            doctor_details.city = request.POST['city']
            doctor_details.state = request.POST['state']
            doctor_details.zip_code = request.POST['zip_code']
            doctor_details.save()
            
            response = redirect('/a/doctors/{0}/?status=1&msg=doctor-created'.format(doctor.id))
            return response
        except Exception as e:
            response = redirect('/a/doctors/create/?status=0&msg=doctor-creation-failed')
            return response
        
        
def EditDoctor(request, id):
    if request.method == 'GET':
        doctor_role = models.Role.objects.get(name='DOCTOR')
        doctor = models.User.objects.get(id=id, role=doctor_role)
        doctor.doctor_details = models.DoctorDetails.objects.get(doctor=doctor)
        context = {
            "doctor": doctor
        }           
        return render(request, 'doctors-edit.html', context)
    elif request.method == 'POST':
        try:
            doctor_role = models.Role.objects.get(name='DOCTOR')
            doctor = models.User.objects.get(id=id, role=doctor_role)
            doctor.first_name = request.POST['first_name']
            doctor.last_name = request.POST['last_name']
            doctor.email = request.POST['email']
            doctor.save()
            # doctor details
            doctor_details = models.DoctorDetails.objects.get(doctor=doctor)
            doctor_details.doctor = doctor
            doctor_details.title = request.POST['title']
            doctor_details.gender = request.POST['gender']
            doctor_details.specialization = request.POST['specialization']
            doctor_details.consultation_fee = request.POST['consultation_fee']
            doctor_details.phone_number = request.POST['phone_number']
            
            doctor_details.address_1 = request.POST['address_1']
            doctor_details.address_2 = request.POST['address_2']
            doctor_details.city = request.POST['city']
            doctor_details.state = request.POST['state']
            doctor_details.zip_code = request.POST['zip_code']
            doctor_details.save()
            response = redirect('/a/doctors/{0}/?status=1&msg=doctor-updated'.format(id))
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/doctors/{0}/?status=0&msg=failed'.format(id))
            return response
        
# Staff
def Staff(request):
    if request.method == 'GET':
        staff_role = models.Role.objects.get(name='STAFF')
        # include staff details model too
        staff_users = models.User.objects.filter(role=staff_role)
        for staff in staff_users:
            print(models.StaffDetails.objects.get(user=staff))
        context = {
            "staff": staff_users
        }
        return render(request, 'staff.html', context)
        
        
def CreateStaff(request):
    # render template
    if request.method == 'GET':
        return render(request, 'staff-create.html')
    # create role
    elif request.method == 'POST':
        try:
            # get STAFF role
            role = models.Role.objects.get(name='STAFF')
            # create role
            staff = models.User()
            staff.first_name = request.POST['first_name']
            staff.last_name = request.POST['last_name']
            staff.email = request.POST['email']
            staff.password = request.POST['password']
            staff.role = role
            staff.save()
            # staff details
            staff_details = models.StaffDetails()
            staff_details.user = staff
            staff_details.department = request.POST['department']
            staff_details.phone_number = request.POST['phone_number']
            
            staff_details.address_1 = request.POST['address_1']
            staff_details.address_2 = request.POST['address_2']
            staff_details.city = request.POST['city']
            staff_details.state = request.POST['state']
            staff_details.zip_code = request.POST['zip_code']
            staff_details.save()
            
            response = redirect('/a/staff/{0}/?status=1&msg=staff-created'.format(staff.id))
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/staff/create/?status=0&msg=staff-creation-failed')
            return response
        
        
def EditStaff(request, id):
    if request.method == 'GET':
        staff_role = models.Role.objects.get(name='STAFF')
        staff = models.User.objects.get(id=id, role=staff_role)
        staff.staff_details = models.StaffDetails.objects.get(user=staff)
        context = {
            "staff": staff
        }           
        return render(request, 'staff-edit.html', context)
    elif request.method == 'POST':
        try:
            staff_role = models.Role.objects.get(name='STAFF')
            staff = models.User.objects.get(id=id, role=staff_role)
            staff.first_name = request.POST['first_name']
            staff.last_name = request.POST['last_name']
            staff.email = request.POST['email']
            staff.save()
            # staff details
            staff_details = models.StaffDetails.objects.get(user=staff)
            staff_details.user = staff
            staff_details.phone_number = request.POST['phone_number']
            staff_details.department = request.POST['department']
        
            
            staff_details.address_1 = request.POST['address_1']
            staff_details.address_2 = request.POST['address_2']
            staff_details.city = request.POST['city']
            staff_details.state = request.POST['state']
            staff_details.zip_code = request.POST['zip_code']
            staff_details.save()
            response = redirect('/a/staff/{0}/?status=1&msg=staff-updated'.format(id))
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/staff/{0}/?status=0&msg=failed'.format(id))
            return response


# Patient
def Patient(request):
    if request.method == 'GET':
        # include staff details model too
        patients = models.Patient.objects.all()
        context = {
            "patients": patients
        }
        return render(request, 'patient.html', context)
        
        
def CreatePatient(request):
    # render template
    if request.method == 'GET':
        return render(request, 'patient-create.html')
    elif request.method == 'POST':
        try:
            # create patient
            patient = models.Patient()
            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.email = request.POST['email']
            patient.phone_number = request.POST['phone_number']
            patient.gender = request.POST['gender']
            patient.allergies = request.POST['allergies']
            patient.medications = request.POST['medications']
            patient.smoking_status = request.POST['smoking_status']
            patient.alcohol_status = request.POST['alcohol_status']
            patient.address_1 = request.POST['address_1']
            patient.address_2 = request.POST['address_2']
            patient.city = request.POST['city']
            patient.state = request.POST['state']
            patient.zip_code = request.POST['zip_code']
            patient.save()

            response = redirect('/a/patient/{0}/?status=1&msg=patient-created'.format(patient.id))
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/patient/create/?status=0&msg=patient-creation-failed')
            return response
        
        
def EditPatient(request, id):
    if request.method == 'GET':
        patient = models.Patient.objects.get(id=id)
        context = {
            "patient": patient
        }           
        return render(request, 'patient-edit.html', context)
    elif request.method == 'POST':
        try:
            patient = models.Patient.objects.get(id=id)
            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.email = request.POST['email']
            patient.phone_number = request.POST['phone_number']
            patient.gender = request.POST['gender']
            patient.allergies = request.POST['allergies']
            patient.medications = request.POST['medications']
            patient.smoking_status = request.POST['smoking_status']
            patient.alcohol_status = request.POST['alcohol_status']
            patient.address_1 = request.POST['address_1']
            patient.address_2 = request.POST['address_2']
            patient.city = request.POST['city']
            patient.state = request.POST['state']
            patient.zip_code = request.POST['zip_code']
            patient.save()
            response = redirect('/a/patient/{0}/?status=1&msg=patient-updated'.format(id))
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/patient/{0}/?status=0&msg=failed'.format(id))
            return response



# Appointment
def Appointment(request):
    if request.method == 'GET':
        # include staff details model too
        data = models.Appointment.objects.all()
        context = {
            "data": data
        }
        return render(request, 'appointments.html', context)
        
        
        
def CreateAppointment(request):
    # render template
    if request.method == 'GET':
        doctors = models.User.objects.filter(role__name='DOCTOR')
        patients = models.Patient.objects.all()
        
        context = {
            "doctors": doctors,
            "patients": patients
        }
        return render(request, 'appointments-create.html', context)
    elif request.method == 'POST':
        try:
            patient = models.Patient.objects.get(id=request.POST['patient'])
            doctor = models.User.objects.get(id=request.POST['doctor'])
            if doctor == None or patient == None:
                response = redirect('/a/appointments/create/?status=0&msg=failed')
                return response
            # create appointment
            appointment = models.Appointment()
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.amount = request.POST['amount']
            appointment.date_time = request.POST['date_time']
            appointment.payment_method = request.POST['payment_method']
            appointment.payment_status = request.POST['payment_status']
            appointment.status = 'PENDING'
            appointment.save()
            response = redirect('/a/appointments/{0}/?status=1&msg=appointment-created'.format(appointment.id))
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/appointments/create/?status=0&msg=patient-creation-failed')
            return response
        
def EditAppointment(request, id):
    # render template
    if request.method == 'GET':
        appointment = models.Appointment.objects.get(id=id)
        doctors = models.User.objects.filter(role__name='DOCTOR')
        patients = models.Patient.objects.all()
        records = models.HealthRecord.objects.filter(appointment__id=id)
        # sample datetime format: 2022-10-13T23:24
        appointment.date_time = appointment.date_time.strftime("%Y-%m-%dT%H:%M")
        
        context = {
            "doctors": doctors,
            "patients": patients,
            "appointment": appointment,
            "records": records
        }
        return render(request, 'appointments-edit.html', context)
    elif request.method == 'POST':
        try:
            appointment = models.Appointment.objects.get(id=id)
            patient = models.Patient.objects.get(id=request.POST['patient'])
            doctor = models.User.objects.get(id=request.POST['doctor'])
            if doctor == None or patient == None:
                response = redirect('/a/appointments/create/?status=0&msg=failed')
                return response
            # create appointment
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.amount = request.POST['amount']
            appointment.date_time = request.POST['date_time']
            appointment.payment_method = request.POST['payment_method']
            appointment.payment_status = request.POST['payment_status']
            appointment.save()
            response = redirect('/a/appointments/{0}/?status=1&msg=appointment-updated'.format(patient.id))
            return response
        except Exception as e:
            print(e)
            response = redirect('/a/appointments/create/?status=0&msg=patient-creation-failed')
            return response


# Inventory

def Inventory(request):
    if request.method == 'GET':
        data = models.Inventory.objects.all()
        context = {
            "data": data
        }
        return render(request, 'inventory.html', context)
    
def CreateInventory(request):
    # render template
    if request.method == 'GET':
        return render(request, 'inventory-create.html')
    # create role
    elif request.method == 'POST':
        try:
            # create role
            inventory = models.Inventory()
            inventory.name = request.POST['name']
            inventory.description = request.POST['description']
            inventory.quantity = request.POST['quantity']
            inventory.save()
            response = redirect('/a/inventory/{0}/?status=1&msg=inventory-created'.format(inventory.id))
            return response
        except Exception as e:
            print("error: ", e)
            response = redirect('/a/inventory/create/?status=0&msg=inventory-create-failed')
            return response    

def EditInventory(request, id):
    if request.method == 'GET':
        data = models.Inventory.objects.get(id=id)
        context = {
            "data": data,
            "type": data.type
        }           
        return render(request, 'inventory-edit.html', context)
    elif request.method == 'POST':
        try:
            inventory = models.Inventory.objects.get(id=id)
            inventory.name = request.POST['name']
            inventory.description = request.POST['description']
            quantity = request.POST['quantity']
            inventory.type = request.POST['category']
            if quantity != '' or quantity != None or quantity <= 0:
                inventory.quantity = quantity
            else:
                response = redirect('/a/inventory/{0}/?status=0&msg=invalid-quantity'.format(id))
                return response
            inventory.save()
            response = redirect('/a/inventory/{0}/?status=1&msg=inventory-updated'.format(id))
            return response
        except Exception as e:
            print("error: ", e)
            response = redirect('/a/inventory/{0}/?status=0&msg=failed'.format(id))
            return response
        
# Records
def Records(request):
    record = models.HealthRecord()
    record_id = request.POST['record_id']
    if int(record_id):
        record = models.HealthRecord.objects.get(id=int(record_id))
    record.patient = models.Patient.objects.get(id=request.POST['patient'])
    record.appointment = models.Appointment.objects.get(id=request.POST['appointment'])
    record.title = request.POST['title']
    record.description = request.POST['description']
    record.save()
    response = redirect('/a/appointments/{0}/?status=1&msg=record-created'.format(record.appointment.id))
    return response


def Prescription(request, id):
    print(id)
    if request.method == 'GET':
        data = models.Prescription.objects.filter(appointment__id=id)
        context = {
            "id": id,
            "data": data
        }
        return render(request, 'prescription.html', context)
    elif request.method == 'POST':
        try:
            prescription = models.Prescription()
            prescription_id = request.POST['prescription_id']
            if int(prescription_id):
                prescription = models.Prescription.objects.get(id=int(prescription_id))
            prescription.appointment = models.Appointment.objects.get(id=id)
            prescription.name = request.POST['name']
            prescription.usage = request.POST['usage']
            prescription.description = request.POST['description']
            prescription.save()
            response = redirect('/a/appointments/{0}/prescription/?status=1&msg=prescription-created'.format(id))
            return response
        except Exception as e:
            print("error: ", e)
            response = redirect('/a/appointments/{0}/prescription/?status=0&msg=prescription-create-failed'.format(id))
            return response