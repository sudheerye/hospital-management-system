from django.db import models

# Create your models here.
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class DoctorDetails(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    consultation_fee = models.FloatField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StaffDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    allergies = models.CharField(max_length=50)
    medications = models.CharField(max_length=50)
    smoking_status = models.CharField(max_length=50)
    alcohol_status = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.FloatField(default=0)
    type = models.CharField(max_length=50, default='MEDICINE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(max_length=50)
    date_time = models.DateTimeField()
    payment_method = models.CharField(max_length=50)
    # PENDING | COMPLETED 
    payment_status = models.CharField(max_length=50, default='PENDING')
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class HealthRecord(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    usage = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)