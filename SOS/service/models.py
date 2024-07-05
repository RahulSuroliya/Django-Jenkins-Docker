from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    login_id = models.EmailField()
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default = '')
    gender = models.CharField(max_length=50,default='')
    mobilenumber = models.CharField(max_length=50,default='')
    role_Id = models.IntegerField()
    role_Name = models.CharField(max_length=50)

    # def to_json(self):
    #     data = {
    #         'id': self.id,
    #         'firstName': self.firstName,
    #         'lastName': self.lastName,
    #         'login_id': self.login_id,
    #         'password': self.password,
    #         'confirmpassword': self.confirmpassword,
    #         'dob': self.dob,
    #         'address': self.address,
    #         'gender': self.gender,
    #         'mobilenumber': self.mobilenumber,
    #         'role_Id': self.role_Id,
    #         'role_Name': self.role_Name
    #     }

    #     return data

    class Meta:
        db_table = 'sos_user'

class Admission(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    login_id = models.EmailField()
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default = '')
    gender = models.CharField(max_length=50,default='')
    mobilenumber = models.CharField(max_length=50,default='')
    role_Id = models.IntegerField()
    role_Name = models.CharField(max_length=50)
    collageName = models.CharField(max_length=50)
    parent_Names = models.CharField(max_length=50)
    parent_Contact_Number =  models.CharField(max_length=50,default='')
    parent_Occupations = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_ADMISSION'


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'ORS_ROLE'

class College(models.Model):
    collegeName = models.CharField(max_length=50)
    collegeAddress = models.CharField(max_length=50)
    collegeState = models.CharField(max_length=50)
    collegeCity = models.CharField(max_length=20)
    collegePhoneNumber = models.CharField(max_length=20)

    class Meta:
        db_table = 'ORS_COLLEGE'

class Car(models.Model):
    carId = models.IntegerField()
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    dateOfMenufactoring = models.DateField(max_length=20)
    price = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_CAR'

class ShoppingCart(models.Model):
    name = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    date = models.DateField(max_length=20)
    quantity = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_SHOPPINGCART'

class Order(models.Model):
    productName = models.CharField(max_length=50)
    orderDate = models.DateField(max_length=20)
    quantity = models.IntegerField()
    customer = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_ORDER'

class Followup(models.Model):
    patient = models.CharField(max_length=50)
    doctor = models.CharField(max_length=50)
    visitDate = models.DateField(max_length=20)
    fees = models.IntegerField()

    class Meta:
        db_table = 'ORS_FOLLOWUP'

class Contact(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobile = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_CONTACT'

class Project(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    openDate = models.DateField(max_length=20)
    version = models.FloatField(max_length=20)

    class Meta:
        db_table = 'ORS_PROJECT'

class Owner(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    vehicleId = models.IntegerField()
    insuranceAmount = models.FloatField()

    class Meta:
        db_table = 'ORS_OWNER'

class Inventory(models.Model):
    supplierName = models.CharField(max_length=50)
    lastUpdatedDate = models.DateField(max_length=20)
    quantity = models.IntegerField()
    product = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_INVENTORY'

class Patient(models.Model):
    name = models.CharField(max_length=50)
    dov = models.DateField(max_length=20)
    mobile = models.CharField(max_length=50)
    decease = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_PATIENT'

# class Model(models.Model):
#     modelType = models.CharField(max_length=100)
#     description = models.CharField(max_length=500)

#     class Meta:
#         db_table = 'ORS_MODEL'

class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseDescription = models.CharField(max_length=100)
    courseDuration = models.CharField(max_length=100)

    class Meta:
        db_table = 'ORS_COURSE'

class Marksheet(models.Model):
    rollNumber = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()

    class Meta:
        db_table = 'ORS_MARKSHEET'

class Student(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobileNumber = models.CharField(max_length=20)
    email = models.EmailField()
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_STUDENT'

class Subject(models.Model):
    SubjectName = models.CharField(max_length=50)
    SubjectDescription = models.CharField(max_length=50)

    Course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_SUBJECT'

class Faculty(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_FACULTY'

class TimeTable(models.Model):
    examTime = models.CharField(max_length=40)
    examDate = models.DateField()
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    class Meta:
        db_table = 'ORS_TIMETABLE'

