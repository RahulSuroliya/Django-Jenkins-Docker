
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Project
from service.forms import ProjectForm
from service.service.Project1Service import Project1Service
# from service.service.ModelService import ModelService

class Project1Ctl(BaseCtl):
    def preload(self, request):
        columnname = ('íd', 'category')
        result= ((1, 'abc'),(2, 'xyz'),(3, 'pqr'),(4, 'jkl'))
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            res["data"].append({columnname[i]:  x[i] for i, _ in enumerate(x)})
        self.page_list = res["data"]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    #populate form from request
    def request_to_form(self, requestForm):
        print("----request_to_form-------------->>called")
        self.form['id']  =  requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['category'] = requestForm['category']
        self.form['openDate'] = requestForm['openDate']
        self.form['version'] = requestForm['version']
        

        
    
    #convert form into model
    def form_to_model(self, obj):
        # c = Project1Service().get(self.form['id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.category = self.form['category']
        obj.openDate = self.form['openDate']
        obj.version = self.form['version']
        
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['category'] = obj.category
        self.form['openDate'] = obj.openDate.strftime("%Y-%m-%d")
        self.form['version'] = obj.version
    
    #ValiopenDate form
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
        
        if DataValidator.isNull(self.form['category']):
            inputError['category'] = "category Can not be Null"
            self.form['error'] = True
        
            
        
        
            
        
        if DataValidator.isNull(self.form['openDate']):
            inputError['openDate'] = "openDate can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['openDate']):
                inputError['openDate'] = "Incorrect Date format, should be DD-MM-YYYY format and openDate should in past or present"
                self.form['error'] = True


        if DataValidator.isNull(self.form['version']):
            inputError['version'] = "Version can't be NUll"
            self.form['error'] = True
        elif (DataValidator.is_float_0(self.form['version'])):
            inputError['version'] = "Version cannot start from 0 or less"
            self.form['error'] =  True
        elif (DataValidator.isflt(self.form['version'])):
            inputError['version'] = "Version should be in float"
            self.form['error'] =  True
        else:
            if DataValidator.max_len_10(self.form['version']):
               inputError['version'] = "Version should of 10 in length max"
               self.form['error'] =  True 
             
        return self.form['error']

    # Display Project1 Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),{'form':self.form,'categoryList':self.preloadData})
        return res

    # Submit Project1Project1 Page
    def submit(self, request, params={}):
        print("----submit---------------->>called")
        if(params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(name = self.form['name'])
            print("-------dup-->>",dup)
            print("-------dup.count()-->>",dup.count())
            if dup.count()>0:
                self.form['error'] = True
                self.form['message'] = "Project1 already exists"
                res = render(request, self.get_template(), {'form': self.form, 'categoryList': self.preloadData})
            else:
                r = self.form_to_model(Project())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form':self.form,'categoryList':self.preloadData})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(name = self.form['name'])
            print("-------duplicate-->>",duplicate)
            print("-----duplicate.count()-->>",duplicate.count())
            if duplicate.count()>0:
                self.form['error'] = True
                self.form['message'] = "Project1 already exists"
                res = render(request, self.get_template(), {'form': self.form, 'categoryList': self.preloadData})
            else:
                r = self.form_to_model(Project())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['message'] = False
                self.form['message'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form':self.form,'categoryList':self.preloadData})
                # res = render(request, self.get_template())
            return res

    # Template html of Project1 Page
    def get_template(self):
        return "Project1.html"

    def get_service(self):
        return Project1Service()
