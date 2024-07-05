
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Inventory
from service.forms import InventoryForm
from service.service.InventoryService import InventoryService
# from service.service.ModelService import ModelService

class InventoryCtl(BaseCtl):
    def preload(self, request):
        self.page_list = [{'product':'mobile'},
                          {'product':'speaker'},
                          {'product':'laptop cleaner'},
                          {'product':'charger'},
                          {'product':'laptop'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")
        self.form['id']  =  requestForm['id']
        self.form['supplierName'] = requestForm['supplierName']
        self.form['lastUpdatedDate'] = requestForm['lastUpdatedDate']
        self.form['quantity'] = requestForm['quantity']
        self.form['product'] = requestForm['product']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = InventoryService().get(self.form['id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.supplierName = self.form['supplierName']
        obj.lastUpdatedDate = self.form['lastUpdatedDate']
        obj.quantity = self.form['quantity']
        obj.product = self.form['product']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['supplierName'] = obj.supplierName
        self.form['lastUpdatedDate'] = obj.lastUpdatedDate.strftime("%Y-%m-%d")
        self.form['quantity'] = obj.quantity
        self.form['product'] = obj.product
    
    #ValilastUpdatedDate form
    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['supplierName']):
            inputError['supplierName'] = "Supplier Name can not be Null"
            self.form['error'] = True
        elif (DataValidator.isalphacheck(self.form['supplierName'])):
                inputError['supplierName'] = "Supplier Name contains only letters"
                self.form['error'] = True
        else:
            if DataValidator.max_len_50(self.form['supplierName']):
                inputError['supplierName'] = "Supplier Name can only be of 50 Characters"
                self.form['error'] = True 

        if DataValidator.isNull(self.form['lastUpdatedDate']):
            inputError['lastUpdatedDate'] = "Last Updated Date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['lastUpdatedDate']):
                inputError['lastUpdatedDate'] = "Incorrect Date format, should be DD-MM-YYYY format and lastUpdatedDate should in past or present"
                self.form['error'] = True          
        
        if DataValidator.isNull(self.form['product']):
            inputError['product'] = "product Can not be Null"
            self.form['error'] = True 
        


        if DataValidator.isNull(self.form['quantity']):
            inputError['quantity'] = "Quantity can't be NUll"
            self.form['error'] = True
        elif (DataValidator.is_float_0(self.form['quantity'])):
            inputError['quantity'] = "Quantity cannot start from 0 or less"
            self.form['error'] =  True
        elif (DataValidator.is_0(self.form['quantity'])):
            inputError['quantity'] = "Quantity should be in Number"
            self.form['error'] =  True
        else:
            if DataValidator.max_len_10(self.form['quantity']):
               inputError['quantity'] = "Quantity should of 10 in length max"
               self.form['error'] =  True 
             
        return self.form['error']

    # Display Inventory Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'productList':self.preloadData})
        return res

    # Submit InventoryInventory Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            r = self.form_to_model(Inventory())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['error'] = False
            self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'productList':self.preloadData})
            return res
        else:            
            r = self.form_to_model(Inventory())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['message'] = False
            self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'productList':self.preloadData})
            # res = render(request, self.get_template())
            return res

    # Template html of Inventory Page
    def get_template(self):
        return "Inventory.html"

    def get_service(self):
        return InventoryService()
