
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Order
from service.forms import OrderForm
from service.service.OrderService import OrderService
# from service.service.ModelService import ModelService

class OrderCtl(BaseCtl):
    def preload(self, request):
        self.page_list = [{'customer':'Rajat'},{'customer':'Jalaj'},{'customer':'Jitesh'},{'customer':'Aman'},{'customer':'Ajay'},{'customer':'Tarun'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")
        self.form['id']  =  requestForm['id']
        self.form['productName'] = requestForm['productName']
        self.form['orderDate'] = requestForm['orderDate']
        self.form['quantity'] = requestForm['quantity']
        self.form['customer'] = requestForm['customer']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = OrderService().get(self.form['id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.productName = self.form['productName']
        obj.orderDate = self.form['orderDate']
        obj.quantity = self.form['quantity']
        obj.customer = self.form['customer']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['productName'] = obj.productName
        self.form['orderDate'] = obj.orderDate.strftime("%Y-%m-%d")
        self.form['quantity'] = obj.quantity
        self.form['customer'] = obj.customer
    
    #Validob form
    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['productName']):
            inputError['productName'] = "productName can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.max_len_50(self.form['productName']):
                inputError['productName'] = "productName can only be of 50 Characters"
                self.form['error'] = True       
        
        if DataValidator.isNull(self.form['customer']):
            inputError['customer'] = "Customer Can not be Null"
            self.form['error'] = True
        
            
        
        
            
        
        if DataValidator.isNull(self.form['orderDate']):
            inputError['orderDate'] = "OrderDate can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['orderDate']):
                inputError['orderDate'] = "Incorrect Date format, should be DD-MM-YYYY format and orderDate should in past or present"
                self.form['error'] = True


        if DataValidator.isNull(self.form['quantity']):
            inputError['quantity'] = "quantity can't be NUll"
            self.form['error'] = True
        elif (DataValidator.is_float_0(self.form['quantity'])):
            inputError['quantity'] = "quantity cannot start from 0 or less"
            self.form['error'] =  True
        elif (DataValidator.isnumb(self.form['quantity'])):
            inputError['quantity'] = "quantity should be in numbers"
            self.form['error'] =  True
        else:
            if DataValidator.max_len_20(self.form['quantity']):
               inputError['quantity'] = "quantity should of 20 in length max"
               self.form['error'] =  True 
             
        return self.form['error']

    # Display Order Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'customerList':self.preloadData})
        return res

    # Submit OrderOrder Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            r = self.form_to_model(Order())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['error'] = False
            self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'customerList':self.preloadData})
            return res
        else:            
            r = self.form_to_model(Order())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['message'] = False
            self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'customerList':self.preloadData})
            # res = render(request, self.get_template())
            return res

    # Template html of Order Page
    def get_template(self):
        return "Order.html"

    def get_service(self):
        return OrderService()
