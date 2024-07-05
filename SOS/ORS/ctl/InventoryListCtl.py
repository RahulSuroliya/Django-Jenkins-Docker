from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import InventoryForm
from service.models import Inventory
from service.service.InventoryService import InventoryService

class InventoryListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        self.page_list = [{'product':'mobile'},{'product':'speaker'},{'product':'laptop cleaner'},{'product':'charger'},{'product':'laptop'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        self.form['supplierName'] = requestForm.get('supplierName', None)
        self.form['lastUpdatedDate'] = requestForm.get('lastUpdatedDate', None)
        self.form['product'] = requestForm.get('product', None)
        self.form['quantity'] = requestForm.get('quantity', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']           
        
        if DataValidator.isNotNull(self.form['supplierName']):
            if (DataValidator.isalphacheck(self.form['supplierName'])):
                inputError['supplierName'] = "supplierName contains only letters"
                self.form['error'] = True
            else:
                if DataValidator.max_len_50(self.form['supplierName']):
                    inputError['supplierName'] = "supplierName can only be of 50 Characters"
                    self.form['error'] = True 
        
        if DataValidator.isNotNull(self.form['lastUpdatedDate']):
            if DataValidator.isDate(self.form['dov']):
                inputError['dov'] = "Incorrect Date format, should be DD-MM-YYYY format and dov should in past or present"
                self.form['error'] = True
    

        if DataValidator.isNotNull(self.form['quantity']):
            if (DataValidator.is_0(self.form['quantity'])):
                inputError['quantity'] = "quantity cannot start from 0 or less"
                self.form['error'] =  True
            elif (DataValidator.isnumb(self.form['quantity'])):
                inputError['quantity'] = "quantity should be in numbers"
                self.form['error'] =  True
            else:
                if DataValidator.max_len_10(self.form['quantity']):
                   inputError['quantity'] = "quantity should of 10 in length max"
                   self.form['error'] =  True 
             
        return self.form['error']

    def display(self, request, params={}):
        InventoryListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        
        res = render(request, self.get_template(), {'pageList':self.page_list,'form':self.form,'productList':self.preloadData})
        return res

    def next(self, request, params={}):
        InventoryListCtl.count += 1
        self.form['pageNo'] = InventoryListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'productList':self.preloadData})
        return res

    def previous(self, request, params={}):
        InventoryListCtl.count -= 1
        self.form['pageNo'] = InventoryListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'productList':self.preloadData})
        return res

    def submit(self, request, params={}):
        InventoryListCtl.count = 1
        record = self.get_service().search1(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'productList':self.preloadData})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = InventoryListCtl.count
        if (bool(self.form['ids']) == False):
            print("qqqqqaaaaaaaaaaaaaaaaaaaaaaaqqqq ")
            self.form['error'] = True
            self.form['messege'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'productList':self.preloadData})
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
                        InventoryListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'productList':self.preloadData})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETED"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'productList':self.preloadData})
        return res


    # Template html of Inventory List Page
    def get_template(self):
        return "InventoryList.html"

    def get_service(self):
        return InventoryService()