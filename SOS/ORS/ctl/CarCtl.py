
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Car
from service.forms import CarForm
from service.service.CarService import CarService
# from service.service.ModelService import ModelService

class CarCtl(BaseCtl):
    def preload(self, request):
        self.page_list = CarService().preload()
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")
        self.form['id']  =  requestForm['id']
        self.form['carId'] = requestForm['carId']
        self.form['brand'] = requestForm['brand']
        self.form['model'] = requestForm['model']
        self.form['dateOfMenufactoring'] = requestForm['dateOfMenufactoring']
        self.form['price'] = requestForm['price']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = CarService().get(self.form['id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.carId = self.form['carId']
        obj.brand = self.form['brand']
        obj.model = self.form['model']
        obj.dateOfMenufactoring = self.form['dateOfMenufactoring']
        obj.price = self.form['price']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['carId'] = obj.carId
        self.form['brand'] = obj.brand
        self.form['model'] = obj.model
        self.form['dateOfMenufactoring'] = obj.dateOfMenufactoring.strftime("%Y-%m-%d")
        self.form['price'] = obj.price
    
    #Validate form
    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['carId']):
            inputError['carId'] = "CarId can not be Null"
            self.form['error'] = True
        
        
        
        if DataValidator.isNull(self.form['brand']):
            inputError['brand'] = "brand Can not be Null"
            self.form['error'] = True
        
        if (DataValidator.isNull(self.form['model'])):
            inputError['model'] = "model can not be null"
            self.form['error'] = True
        # else:
        #     o = CarService().find_by_unique_key(self.form['id'])
        #     print("------o-->>",o)
        #     self.form['model'] = o.model
            
        
        if DataValidator.isNull(self.form['dateOfMenufactoring']):
            inputError['dateOfMenufactoring'] = "dateOfMenufactoring can not be Null"
            self.form['error'] = True

        if DataValidator.isNull(self.form['price']):
            inputError['price'] = "price can't be NUll"
            self.form['error'] = True
        else:
            if DataValidator.isno(self.form['price']):
               inputError['price'] = "price shuld be in no's"
               self.form['error'] = True      
        return self.form['error']

    # Display Car Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'carList':self.preloadData})
        return res

    # Submit CarCar Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(carId=self.form['carId'])
            if dup.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Car Id Already Exist"
                res = render(request, self.get_template(), {'form':self.form,'carList':self.preloadData})
            else:
                r = self.form_to_model(Car())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form':self.form,'carList':self.preloadData})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(carId=self.form['carId'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Car Id Already Exists"
                res = render(request, self.get_template(), {'form':self.form,'carList':self.preloadData})
            else:
                r = self.form_to_model(Car())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['message'] = False
                self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form':self.form,'carList':self.preloadData})
                # res = render(request, self.get_template())

            return res

    # Template html of Car Page
    def get_template(self):
        return "Car.html"

    def get_service(self):
        return CarService()
