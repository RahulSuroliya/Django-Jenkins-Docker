from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import Admission
from service.service.AdmissionService import AdmissionService
from service.service.CollegeService import CollegeService

class AdmissionListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        self.page_list = AdmissionService().preload()
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        print("------request_to_form--self,requestForm>>",self,requestForm)
        self.form['firstName'] = requestForm.get("firstName", None)
        self.form['lastName'] = requestForm.get("lastName", None)
        self.form['login_id'] = requestForm.get("login_id", None)
        self.form['role_Name'] = requestForm.get("role_Name", None)
        self.form['collageName'] = requestForm.get("collageName", None)
        self.form['dob'] = requestForm.get("dob", None)
        self.form['ids'] = requestForm.get("ids", None)

    def display(self, request, params={}):
        print("-----display-self,request,params-->>",self,request,params)
        AdmissionListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']

        self.form['lastId'] = Admission.objects.last().id 
        res = render(request, self.get_template(), {'pageList':self.page_list, "form": self.form,"admissionList":self.preloadData})
        return res

    def next(self, request, params={}):
        print("-------next-->self,request,params-->>",self,request,params)
        AdmissionListCtl.count += 1
        self.form['pageNo'] = AdmissionListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Admission.objects.last().id
        res = render(request, self.get_template(), {"pageList":self.page_list, "form":self.form})
        return res

    def previous(self, request, params={}):
        print("-------previous-->self,request,params-->>",self,request,params)
        AdmissionListCtl.count -= 1
        self.form['pageNo'] = AdmissionListCtl.count
        print("-----self.form['pageNo']-->>",self.form['pageNo'])
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def deleteRecord(self, request, params={}):
        print("------deleteRecord(self, request, params={}):--->>",self, request, params)
        self.form['pageNo'] = AdmissionListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            print("---if(record)--self.page_list-->>",self.page_list)
            res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        else:
            for ids in self.form['ids']:
                print("-----ids-->>",ids)
                record = self.get_service().search(self.form)
                self.page_list = record['data']
                id = int(ids)
                if (id>0):
                    r = self.get_service().get(id)
                    print("----r-->>",r)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = Admission.objects.last().id
                        AdmissionListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def submit(self, request, params={}):
        print("------submit(self, request, params={}):-->>",self, request, params)
        AdmissionListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def get_template(self):
        return "AdmissionList.html"

    def get_service(self):
        return AdmissionService()