from ast import Try
from .BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from django.shortcuts import render
from service.forms import PatientForm
from service.models import Patient
from service.service.PatientService import PatientService
# from service.service.ModelService import ModelService

class PatientListCtl(BaseCtl):
    count = 1
    
    def preload(self, request):
        self.page_list = [{'decease':'Allergies'},{'decease':'Colds and Flu'},{'decease':'Conjunctivitis'},{'decease':'Diarrhea'},{'decease':'Stomach Aches'},{'decease':'Headaches'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get("name", None)
        self.form['dov'] = requestForm.get("dov", None)
        self.form['mobile'] = requestForm.get("mobile", None)
        self.form['decease'] = requestForm.get("decease", None)
        self.form['ids'] = requestForm.get("ids", None)

    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNotNull(self.form['name']):
            if (DataValidator.isalphacheck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True
            else:
                if DataValidator.max_len_50(self.form['name']):
                    inputError['name'] = "Name can only be of 50 Characters"
                    self.form['error'] = True             
        
        if DataValidator.isNotNull(self.form['dov']):
            if DataValidator.isDate(self.form['dov']):
                inputError['dov'] = "dov should in past or present"
                self.form['error'] = True

        if DataValidator.isNotNull(self.form['mobile']):
            if (DataValidator.ismobilecheck(self.form['mobile'])):
                inputError['mobile'] = "Mobile No. should start with 6,7,8,9 and no. must be of 10 digits"
                self.form['error'] =  True    
             
        return self.form['error']

        

    def display(self, request, params={}):
        PatientListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Patient.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'deceaseList':self.preloadData})
        return res

    def previous(self, request, params={}):
        PatientListCtl.count -= 1
        self.form['pageNo'] = PatientListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'deceaseList':self.preloadData})
        return res

    def next(self, request, params={}):
        PatientListCtl.count += 1
        self.form['pageNo'] = PatientListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Patient.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'deceaseList':self.preloadData})
        return res

    def submit(self, request, params={}):     
        PatientListCtl.count = 1
        record = self.get_service().search1(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found / Provide with correct value"
        ress = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'deceaseList':self.preloadData})
        return ress

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = PatientListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please select atleast one checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'deceaseList':self.preloadData})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if(id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = Patient.objects.last().id
                        PatientListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        print("ppppppppp----->>", self.page_list)
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'deceaseList':self.preloadData})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'deceaseList':self.preloadData})
        return res

    def get_template(self):
        return "PatientList.html"

    def get_service(self):
        return PatientService()
