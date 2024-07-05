
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Followup
from service.forms import FollowupForm
from service.service.FollowupService import FollowupService
# from service.service.ModelService import ModelService

class FollowupCtl(BaseCtl):
    def preload(self, request):
        self.page_list = [{'doctor':'Rajat','patient':'Raj'},{'doctor':'Jal','patient':'Jalaj'},{'doctor':'Jite','patient':'Jitesh'},{'doctor':'Aman','patient':'man'},{'doctor':'Ajay','patient':'Aj'},{'doctor':'Tarun','patient':'Taun'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")
        self.form['id']  =  requestForm['id']
        self.form['patient'] = requestForm['patient']
        self.form['doctor'] = requestForm['doctor']
        self.form['visitDate'] = requestForm['visitDate']
        self.form['fees'] = requestForm['fees']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = FollowupService().get(self.form['id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.patient = self.form['patient']
        obj.doctor = self.form['doctor']
        obj.visitDate = self.form['visitDate']
        obj.fees = self.form['fees']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['patient'] = obj.patient
        self.form['doctor'] = obj.doctor
        self.form['visitDate'] = obj.visitDate.strftime("%Y-%m-%d")
        self.form['fees'] = obj.fees
    
    #Validob form
    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['patient']):
            inputError['patient'] = "patient can not be Null"
            self.form['error'] = True          
        
        if DataValidator.isNull(self.form['doctor']):
            inputError['doctor'] = "doctor Can not be Null"
            self.form['error'] = True            
        
        if DataValidator.isNull(self.form['visitDate']):
            inputError['visitDate'] = "visitDate can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDatefuture(self.form['visitDate']):
                inputError['visitDate'] = "Incorrect Date format, should be DD-MM-YYYY format "
                self.form['error'] = True


        if DataValidator.isNull(self.form['fees']):
            inputError['fees'] = "fees can't be NUll"
            self.form['error'] = True
        elif (DataValidator.is_0(self.form['fees'])):
            inputError['fees'] = "fees cannot start from 0 or less"
            self.form['error'] =  True
        elif (DataValidator.isnumb(self.form['fees'])):
            inputError['fees'] = "fees should be in numbers"
            self.form['error'] =  True
        else:
            if DataValidator.max_len_10(self.form['fees']):
               inputError['fees'] = "fees should of 10 in length max"
               self.form['error'] =  True 
             
        return self.form['error']

    # Display Followup Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
        return res

    # Submit FollowupFollowup Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            r = self.form_to_model(Followup())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['error'] = False
            self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
            return res
        else:            
            r = self.form_to_model(Followup())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['message'] = False
            self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
            # res = render(request, self.get_template())
            return res

    # Template html of Followup Page
    def get_template(self):
        return "Followup.html"

    def get_service(self):
        return FollowupService()
