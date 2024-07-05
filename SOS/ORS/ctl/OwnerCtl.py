
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Owner
from service.forms import OwnerForm
from service.service.OwnerService import OwnerService
# from service.service.ModelService import ModelService
from datetime import date

class OwnerCtl(BaseCtl):
    x=None
    y=None  
    def preload(self, request):
        self.page_list = [
                          { 'vid': 1, 'vehicleId' : 1001 },
                          { 'vid': 2, 'vehicleId' : 1002 },
                          { 'vid': 3, 'vehicleId' : 1003 },
                          { 'vid': 4, 'vehicleId' : 1004 },
                          { 'vid': 5, 'vehicleId' : 1005 },
                          { 'vid': 6, 'vehicleId' : 1006 }
                        ]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def preload1(self, request):
        self.page_list = [
                           { 'did': 1, 'dob' : '2001-05-11' },
                           { 'did': 2, 'dob' : '1999-07-14' },
                           { 'did': 3, 'dob' : '1995-01-01' },
                           { 'did': 4, 'dob' : '2004-07-07' },
                           { 'did': 5, 'dob' : '2005-08-12' },
                           { 'did': 6, 'dob' : '2000-11-25' }
                         ]
        print("-----preload--self.page_list",self.page_list)
        self.preload1Data = self.page_list
    
    def find_dict_index(self,dict_list, key, value):
        for index, item in enumerate(dict_list):
            if int(item.get(key)) == int(value):
                print('--------------',index)
                return index
            
    def get_key_from_value(self, target_key, target_value, result_key):
        for item in self.preload1Data:
            if item.get(target_key) == target_value:
                return item.get(result_key)

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")

        index = self.find_dict_index(self.preloadData, 'vid', requestForm['vehicleId'])
        index1 = self.find_dict_index(self.preload1Data, 'did', requestForm['dob'])

        self.form['id']  =  requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['dob'] = self.preload1Data[index1]['dob']
        self.form['vehicleId'] = self.preloadData[index]['vehicleId']
        self.form['insuranceAmount'] = requestForm['insuranceAmount']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = OwnerService().get(self.form['id'])

        
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.dob = self.form['dob']        
        obj.vehicleId = self.form['vehicleId']
        obj.insuranceAmount = self.form['insuranceAmount']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        result_key = self.get_key_from_value('vehicleId', obj.vehicleId , 'vid')
        result_key1 = self.get_key_from_value('dob', obj.dob, 'did')
        print('-------------------',result_key1)
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['dobKey']=result_key1
        self.form['dob'] = obj.dob.strftime("%Y-%m-%d")
        self.form['vehicleIdKey']=result_key
        self.form['vehicleId'] = obj.vehicleId
        self.form['insuranceAmount'] = obj.insuranceAmount
      
    # def preload(self, request):
    #     self.page_list = {
    #                       '1' : 1001,
    #                       '2' : 1002,
    #                       '3' : 1003,
    #                       '4' : 1004,
    #                       '5' : 1005,
    #                       '6' : 1006
    #                      }
    #     print("-----preload--self.page_list",self.page_list)
    #     self.preloadData = self.page_list

    # def preload1(self, request):
    #     self.page_list = {
    #                        '1' : '2001-05-11',
    #                        '2' : '1999-07-14',
    #                        '3' : '1995-01-01',
    #                        '4' : '2004-07-07',
    #                        '5' : '2005-08-12',
    #                        '6' : '2000-11-25'
    #                       }
    #     print("-----preload--self.page_list",self.page_list)
    #     self.preload1Data = self.page_list
    

    # #populate form from request
    # def request_to_form(self, requestForm):
    #     print("----request_to_form-------------->>called")

    #     self.form['id']  =  requestForm['id']
    #     self.form['name'] = requestForm['name']
    #     # self.form['dob'] = self.preload_data2[requestForm['dob']]
    #     self.form['dob'] = self.preload1Data[requestForm['dob']]
    #     self.form['vehicleId'] = self.preloadData[requestForm['vehicleId']]
    #     self.form['insuranceAmount'] = requestForm['insuranceAmount']
        

        
    
    # #convert form into model
    # def form_to_model(self, obj):
    #     # c = OwnerService().get(self.form['id'])

        
    #     pk = int(self.form['id'])
    #     if pk > 0:
    #         obj.id = pk
    #     obj.name = self.form['name']
    #     obj.dob = self.form['dob']        
    #     obj.vehicleId = self.form['vehicleId']
    #     obj.insuranceAmount = self.form['insuranceAmount']
        
    #     return obj
    
    # #populate form form model
    # def model_to_form(self, obj):
    #     if (obj == None):
    #         return
    #     self.form['id'] = obj.id
    #     self.form['name'] = obj.name
    #     y = list(self.preload1Data.keys())[list(self.preload1Data.values()).index(obj.dob.strftime("%Y-%m-%d"))]
    #     self.form['dobKey']=y
    #     self.form['dob'] = obj.dob.strftime("%Y-%m-%d")
    #     x = list(self.preloadData.keys())[list(self.preloadData.values()).index(obj.vehicleId)]
    #     self.form['vehicleIdKey']=x
    #     self.form['vehicleId'] = obj.vehicleId
    #     self.form['insuranceAmount'] = obj.insuranceAmount
    
    #Validate form
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

        if DataValidator.isNull(self.form['dob']):
            inputError['dob'] = "dob can not be Null"
            self.form['error'] = True          
        
        if DataValidator.isNull(self.form['vehicleId']):
            inputError['vehicleId'] = "vehicleId Can not be Null"
            self.form['error'] = True 
        


        if DataValidator.isNull(self.form['insuranceAmount']):
            inputError['insuranceAmount'] = "insuranceAmount can't be NUll"
            self.form['error'] = True
        elif (DataValidator.is_float_0(self.form['insuranceAmount'])):
            inputError['insuranceAmount'] = "insuranceAmount cannot start from 0 or less"
            self.form['error'] =  True
        elif (DataValidator.isflt(self.form['insuranceAmount'])):
            inputError['insuranceAmount'] = "insuranceAmount should be in float"
            self.form['error'] =  True
        else:
            if DataValidator.max_len_10(self.form['insuranceAmount']):
               inputError['insuranceAmount'] = "insuranceAmount should of 10 in length max"
               self.form['error'] =  True 
             
        return self.form['error']

    # Display Owner Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
        return res

    # Submit OwnerOwner Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            r = self.form_to_model(Owner())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['error'] = False
            self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
            return res
        else:            
            r = self.form_to_model(Owner())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['message'] = False
            self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
            res = render(request, self.get_template(), {'form':self.form,'vehicleIdList':self.preloadData,'dobList':self.preload1Data})
            # res = render(request, self.get_template())
            return res

    # Template html of Owner Page
    def get_template(self):
        return "Owner.html"

    def get_service(self):
        return OwnerService()
