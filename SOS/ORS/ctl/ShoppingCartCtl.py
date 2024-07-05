
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import ShoppingCart
from service.forms import ShoppingCartForm
from service.service.ShoppingCartService import ShoppingCartService
# from service.service.ModelService import ModelService

class ShoppingCartCtl(BaseCtl):
    def preload(self, request):
        self.page_list = [{'product':'mobile'},{'product':'speaker'},{'product':'laptop cleaner'},{'product':'charger'},{'product':'laptop'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")
        self.form['id']  =  requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['product'] = requestForm['product']
        self.form['date'] = requestForm['date']
        self.form['quantity'] = requestForm['quantity']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = ShoppingCartService().get(self.form['id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.product = self.form['product']
        obj.date = self.form['date']
        obj.quantity = self.form['quantity']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['product'] = obj.product
        self.form['date'] = obj.date.strftime("%Y-%m-%d")
        self.form['quantity'] = obj.quantity
    
    #Validate form
    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['name']):
            inputError['name'] = "name can not be Null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['name'])):
                inputError['lastName'] = "Name contains only letters"
                self.form['error'] = True
        
        
        
        if DataValidator.isNull(self.form['product']):
            inputError['product'] = "product Can not be Null"
            self.form['error'] = True
        
        
            
        
        if DataValidator.isNull(self.form['date']):
            inputError['date'] = "date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['date']):
                inputError['date'] = "Incorrect date format, should be DD-MM-YYYY format."
                self.form['error'] = True


        if DataValidator.isNull(self.form['quantity']):
            inputError['quantity'] = "quantity can't be NUll"
            self.form['error'] = True
        else:
            if DataValidator.isnumb(self.form['quantity']):
                inputError['quantity'] = "Number shuld be from 0-9"
                self.form['error'] = True
             
        return self.form['error']

    # Display ShoppingCart Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'cartList':self.preloadData})
        return res

    # Submit ShoppingCartShoppingCart Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            r = self.form_to_model(ShoppingCart())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['error'] = False
            self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'cartList':self.preloadData})
            return res
        else:
            r = self.form_to_model(ShoppingCart())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['message'] = False
            self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'cartList':self.preloadData})
            # res = render(request, self.get_template())
            return res

    # Template html of ShoppingCart Page
    def get_template(self):
        return "ShoppingCart.html"

    def get_service(self):
        return ShoppingCartService()
