from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import ProjectForm
from service.models import Project
from service.service.Project1Service import Project1Service

class Project1ListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        self.page_list = [{'category':'Software Development '},{'category':'Cybersecurity'},{'category':'Data Management and Analytics'},{'category':'Cloud Computing'},{'category':'AI and Machine Learning'},{'category':'Network and Telecommunication'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get('name', None)
        self.form['category'] = requestForm.get('category', None)
        self.form['openDate'] = requestForm.get('openDate', None)
        self.form['version'] = requestForm.get('version', None)
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

        if DataValidator.isNotNull(self.form['openDate']):
            if DataValidator.isDate(self.form['openDate']):
                inputError['openDate'] = "Incorrect Date format, should be DD-MM-YYYY format and openDate should in past or present"
                self.form['error'] = True
    

        if DataValidator.isNotNull(self.form['version']):
            if (DataValidator.is_float_0(self.form['version'])):
                inputError['version'] = "version cannot start from 0 or less"
                self.form['error'] =  True
            elif (DataValidator.isflt(self.form['version'])):
                inputError['version'] = "version should be in float"
                self.form['error'] =  True
            else:
                if DataValidator.max_len_10(self.form['version']):
                   inputError['version'] = "version should of 10 in length max"
                   self.form['error'] =  True 
             
        return self.form['error']

    def display(self, request, params={}):
        Project1ListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        
        res = render(request, self.get_template(), {'pageList':self.page_list,'form':self.form,'categoryList':self.preloadData})
        return res

    def next(self, request, params={}):
        Project1ListCtl.count += 1
        self.form['pageNo'] = Project1ListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'categoryList':self.preloadData})
        return res

    def previous(self, request, params={}):
        Project1ListCtl.count -= 1
        self.form['pageNo'] = Project1ListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'categoryList':self.preloadData})
        return res

    def submit(self, request, params={}):
        Project1ListCtl.count = 1
        record = self.get_service().search1(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'categoryList':self.preloadData})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = Project1ListCtl.count
        if (bool(self.form['ids']) == False):
            print("qqqqqaaaaaaaaaaaaaaaaaaaaaaaqqqq ")
            self.form['error'] = True
            self.form['messege'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'categoryList':self.preloadData})
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
                        Project1ListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'categoryList':self.preloadData})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETED"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form,'categoryList':self.preloadData})
        return res


    # Template html of Project List Page
    def get_template(self):
        return "Project1List.html"

    def get_service(self):
        return Project1Service()