from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import Admission
from service.service.AdmissionService import AdmissionService
from service.service.CollegeService import CollegeService

class AdmissionCtl(BaseCtl):
    def preload(self, request):
        self.page_list = CollegeService().preload()
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    # Populate Form from http request
    def request_to_form(self, requestForm):
        print("-----request to form-requestForm['id']",requestForm["id"])
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] = requestForm["dob"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] = 2
        self.form["role_Name"] = 'student'
        self.form["college_Id"] = requestForm["college_Id"]
        self.form["parent_Names"] = requestForm["parent_Names"]
        self.form["parent_Contact_Number"] = requestForm["parent_Contact_Number"]
        self.form["parent_Occupations"] = requestForm["parent_Occupations"]


        

    # Convert Form into module
    def form_to_model(self, obj):
        pk = int(self.form['id'])
        c = CollegeService().get(self.form['college_Id'])
        print("----form to model-C-->>",c)
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"]
        obj.confirmpassword = self.form["confirmpassword"]
        obj.dob = self.form["dob"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.role_Id = self.form["role_Id"]
        obj.role_Name = self.form["role_Name"]
        obj.collageName = c.collegeName
        obj.parent_Names = self.form["parent_Names"]
        obj.parent_Contact_Number = self.form["parent_Contact_Number"]
        obj.parent_Occupations = self.form["parent_Occupations"]

        return obj

    # Populate Form from model
    # GET-DISPLAY method calls this function
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        print("-----obj.id-->>",obj.id)
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["address"] = obj.address  
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["role_Id"] = obj.role_Id
        self.form["role_Name"] = obj.role_Name
        self.form["collageName"] = obj.collageName
        self.form["parent_Names"] = obj.parent_Names
        self.form["parent_Contact_Number"] = obj.parent_Contact_Number
        self.form["parent_Occupations"] = obj.parent_Occupations


    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isalphacheck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True
        
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        else:
                if (DataValidator.isalphacheck(self.form['lastName'])):
                    inputError['lastName'] = "Last Name contains only letters"
                    self.form['error'] = True
        if (DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form['login_id'])):
                inputError['login_id'] = "login ID must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["confirmpassword"])):
            inputError["confirmpassword"] = "Confirm Password can not be null"
            self.form["error"] = True
            
        if (DataValidator.isNotNull(self.form['confirmpassword'])):
            if (self.form['password'] != self.form['confirmpassword']):
                inputError['confirmpassword'] = "Pwd & Confirm Pwd aren't same"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob']= "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True
        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender can not be null"
            self.form['error']  = True
        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobilenumber'])):
                inputError['mobilenumber'] = "Mobile No should start with 6,7,8,9"
                self.form['error'] =  True
        if (DataValidator.isNull(self.form['college_Id'])):
            inputError['college_Id'] = "Collage can not be null"
            self.form['error'] = True
        else:
            o = CollegeService().find_by_unique_key(self.form['college_Id'])
            print("------o-->>",o)
            self.form['collageName'] = o.collegeName
            print("------self.form['collageName']-->>",self.form['collageName'])
        if (DataValidator.isNull(self.form["parent_Names"])):
            inputError["parent_Names"] = "Parents Name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isalphacheck(self.form['parent_Names'])):
                inputError['parent_Names'] = "Parents Name contains only letters"
                self.form['error'] = True
        if (DataValidator.isNull(self.form["parent_Occupations"])):
            inputError["parent_Occupations"] = "Parents Ocupassion can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isalphacheck(self.form['parent_Occupations'])):
                inputError['parent_Occupations'] = "Parents Occupations contains only letters"
                self.form['error'] = True
        if (DataValidator.isNull(self.form["parent_Contact_Number"])):
            inputError["parent_Contact_Number"] = "Mobile Number can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ismobilecheck(self.form['parent_Contact_Number'])):
                inputError['parent_Contact_Number'] = "Mobile No should start with 6,7,8,9"
                self.form['error'] =  True
        return self.form['error']

    # Display Admission Page
    def display(self, request, params={}):
        print("---Admission-Display--self,request,params-->>",self,request,params)
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            print("------r-->>",r)
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.preloadData})
        return res

    # Submit Admission Page
    def submit(self, request, params={}):
        print("------submit--params-->>",params)
        print("------submit--params-->>",params['id'])
        if (params['id'] > 0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(login_id = self.form['login_id'])
            print("-------dup-->>",dup)
            print("-------dup.count()-->>",dup.count())
            if dup.count()>0:
                self.form['error'] = True
                self.form['message'] = "Login Id already exists"
                res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.preloadData})
            else:
                r = self.form_to_model(Admission())
                print("------r-->>",r)
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.preloadData})
        else:
            duplicate = self.get_service().get_model().objects.filter(login_id = self.form['login_id'])
            print("-------duplicate-->>",duplicate)
            print("-----duplicate.count()-->>",duplicate.count())
            if duplicate.count()>0:
                self.form['error'] = True
                self.form['message'] = "Login Id already exists"
                res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.preloadData})
            else:
                r = self.form_to_model(Admission())
                print("------r-->>",r)
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.preloadData})
        return res

    def get_template(self):
        return "Admission.html"

    def get_service(self):
        return AdmissionService()