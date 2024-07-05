from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import OwnerForm
from service.models import Owner
from service.service.OwnerService import OwnerService

class OwnerListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        columnname = ('id', 'vehicleId')
        result= ((1, '1001'),(2, '1002'),(3, '1003'),(4, '1004'),(5, '1005'),(6, '1006'))
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            res["data"].append({columnname[i]:  x[i] for i, _ in enumerate(x)})
        self.page_list = res["data"]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def preload1(self, request):
        columnname = ('id', 'dob')
        result= ((1, '2001-05-11'),(2, '1999-07-14'),(3, '1995-01-01'),(4, '2004-07-07'),(5, '2005-08-12'),(6, '2000-11-25'))
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            res["data"].append({columnname[i]:  x[i] for i, _ in enumerate(x)})
        self.page_list = res["data"]
        print("-----preload--self.page_list",self.page_list)
        self.preload1Data = self.page_list

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get('name', None)
        self.form['dob'] = requestForm.get('dob', None)
        self.form['vehicleId'] = requestForm.get('vehicleId', None)
        self.form['insuranceAmount'] = requestForm.get('insuranceAmount', None)
        self.form['ids'] = requestForm.getlist('ids', None)

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
    

        if DataValidator.isNotNull(self.form['insuranceAmount']):
            if (DataValidator.is_0(self.form['insuranceAmount'])):
                inputError['insuranceAmount'] = "insuranceAmount cannot start from 0 or less"
                self.form['error'] =  True
            elif (DataValidator.isnumb(self.form['insuranceAmount'])):
                inputError['insuranceAmount'] = "insuranceAmount should be in numbers"
                self.form['error'] =  True
            else:
                if DataValidator.max_len_10(self.form['insuranceAmount']):
                   inputError['insuranceAmount'] = "insuranceAmount should of 10 in length max"
                   self.form['error'] =  True 
             
        return self.form['error']

    def display(self, request, params={}):
        OwnerListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        
        res = render(request, self.get_template(), {'pageList':self.page_list,'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
        return res

    def next(self, request, params={}):
        OwnerListCtl.count += 1
        self.form['pageNo'] = OwnerListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
        return res

    def previous(self, request, params={}):
        OwnerListCtl.count -= 1
        self.form['pageNo'] = OwnerListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
        return res

    def submit(self, request, params={}):
        OwnerListCtl.count = 1
        record = self.get_service().search1(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = OwnerListCtl.count
        if (bool(self.form['ids']) == False):
            print("qqqqqaaaaaaaaaaaaaaaaaaaaaaaqqqq ")
            self.form['error'] = True
            self.form['messege'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
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
                        OwnerListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETED"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
        return res


    # Template html of Owner List Page
    def get_template(self):
        return "OwnerList.html"

    def get_service(self):
        return OwnerService()