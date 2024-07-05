
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Contact
from service.forms import ContactForm
from service.service.ContactService import ContactService
# from service.service.ModelService import ModelService

class ContactCtl(BaseCtl):
    def preload(self, request):
        self.page_list = [{'city':'Indore'},{'city':'Mumbai'},{'city':'Delhi'},{'city':'Gurgaon'},{'city':'Pune'},{'city':'Banglore'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")
        self.form['id']  =  requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['city'] = requestForm['city']
        self.form['dob'] = requestForm['dob']
        self.form['mobile'] = requestForm['mobile']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = ContactService().get(self.form['id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.city = self.form['city']
        obj.dob = self.form['dob']
        obj.mobile = self.form['mobile']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['city'] = obj.city
        self.form['dob'] = obj.dob.strftime("%Y-%m-%d")
        self.form['mobile'] = obj.mobile
    
    #Validob form
    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['name']):
            inputError['name'] = "Name can not be Null"
            self.form['error'] = True
        elif (DataValidator.isalphacheck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True
        else:
            if DataValidator.max_len_50(self.form['name']):
                inputError['name'] = "Name can only be of 50 Characters"
                self.form['error'] = True       
        
        if DataValidator.isNull(self.form['city']):
            inputError['city'] = "City Can not be Null"
            self.form['error'] = True
        
            
        
        
            
        
        if DataValidator.isNull(self.form['dob']):
            inputError['dob'] = "Dob can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['dob']):
                inputError['dob'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True


        if DataValidator.isNull(self.form['mobile']):
            inputError['mobile'] = "Mobile No. can't be NUll"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobile'])):
                inputError['mobile'] = "Mobile No. should start with 6,7,8,9 and no. must be of 10 digits"
                self.form['error'] =  True
             
        return self.form['error']

    # Display Contact Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'cityList':self.preloadData})
        return res

    # Submit ContactContact Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(mobile = self.form['mobile'])
            print("-------dup-->>",dup)
            print("-------dup.count()-->>",dup.count())
            if dup.count()>0:
                self.form['error'] = True
                self.form['message'] = "Contact already exists"
                res = render(request, self.get_template(), {'form': self.form, 'cityList': self.preloadData})
            else:
                r = self.form_to_model(Contact())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form':self.form,'cityList':self.preloadData})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(mobile = self.form['mobile'])
            print("-------duplicate-->>",duplicate)
            print("-----duplicate.count()-->>",duplicate.count())
            if duplicate.count()>0:
                self.form['error'] = True
                self.form['message'] = "Contact already exists"
                res = render(request, self.get_template(), {'form': self.form, 'cityList': self.preloadData})
            else:
                r = self.form_to_model(Contact())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['message'] = False
                self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form':self.form,'cityList':self.preloadData})
                # res = render(request, self.get_template())
            return res

    # Template html of Contact Page
    def get_template(self):
        return "Contact.html"

    def get_service(self):
        return ContactService()
