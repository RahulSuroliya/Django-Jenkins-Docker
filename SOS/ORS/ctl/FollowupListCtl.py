from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import FollowupForm
from service.models import Followup
from service.service.FollowupService import FollowupService

class FollowupListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        self.page_list = [{'doctor':'Rajat','patient':'Raj'},{'doctor':'Jal','patient':'Jalaj'},{'doctor':'Jite','patient':'Jitesh'},{'doctor':'Aman','patient':'man'},{'doctor':'Ajay','patient':'Aj'},{'doctor':'Tarun','patient':'Taun'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        self.form['patient'] = requestForm.get('patient', None)
        self.form['doctor'] = requestForm.get('doctor', None)
        self.form['visitDate'] = requestForm.get('visitDate', None)
        self.form['fees'] = requestForm.get('fees', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']           
        
        if DataValidator.isNotNull(self.form['visitDate']):
            if DataValidator.isDatefuture(self.form['visitDate']):
                inputError['visitDate'] = "Incorrect Date format, should be DD-MM-YYYY format "
                self.form['error'] = True


        if DataValidator.isNotNull(self.form['fees']):
            if (DataValidator.is_0(self.form['fees'])):
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

    def display(self, request, params={}):
        FollowupListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        # if self.page_list==[]:
        #     self.form['mesg'] = "No record found"
        res = render(request, self.get_template(), {'pageList':self.page_list,'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
        return res

    def next(self, request, params={}):
        FollowupListCtl.count += 1
        self.form['pageNo'] = FollowupListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        # self.form['LastId'] = Followup.objects.last().id
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
        return res

    def previous(self, request, params={}):
        FollowupListCtl.count -= 1
        self.form['pageNo'] = FollowupListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
        return res

    def submit(self, request, params={}):
        FollowupListCtl.count = 1
        record = self.get_service().search1(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = FollowupListCtl.count
        if (bool(self.form['ids']) == False):
            print("qqqqqaaaaaaaaaaaaaaaaaaaaaaaqqqq ")
            self.form['error'] = True
            self.form['messege'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
        else:
            print("qqqqqqqqqq-------------------------------")
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if (id>0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        # if record['data']==None:
                        #     self.form['LastId'] = Followup.objects.last().id
                        FollowupListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETED"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'doctorList':self.preloadData,'patientList':self.preloadData})
        return res


    # Template html of Followup List Page
    def get_template(self):
        return "FollowupList.html"

    def get_service(self):
        return FollowupService()