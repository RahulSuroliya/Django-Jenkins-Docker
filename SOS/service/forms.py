from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = "__all__"

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = "__all__"


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"

class ShoppingCartForm(forms.ModelForm):
    class Meta:
        model = ShoppingCart
        fields = "__all__"

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class FollowupForm(forms.ModelForm):
    class Meta:
        model = Followup
        fields = "__all__"

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"

# class ModelForm(forms.ModelForm):
#     class Meta:
#         model = Model
#         fields = "__all__"

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = "__all__"

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = "__all__"

class MarksheetForm(forms.ModelForm):
    class Meta:
        model = Marksheet
        fields = "__all__"

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = "__all__"
