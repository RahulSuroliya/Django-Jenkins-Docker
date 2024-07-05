from ast import Try
from .BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from django.shortcuts import render
from service.forms import ContactForm
from service.models import Contact
from service.service.ContactService import ContactService
# from service.service.ModelService import ModelService

class ContactListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        self.page_list = [{'city':'Indore'},{'city':'Mumbai'},{'city':'Delhi'},{'city':'Gurgaon'},{'city':'Pune'},{'city':'Banglore'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get("name", None)
        self.form['city'] = requestForm.get("city", None)
        self.form['dob'] = requestForm.get("dob", None)
        self.form['mobile'] = requestForm.get("mobile", None)
        self.form['ids'] = requestForm.get("ids", None)

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
        
        if DataValidator.isNotNull(self.form['dob']):
            if DataValidator.isDate(self.form['dob']):
                inputError['dob'] = "Dob should in past or present"
                self.form['error'] = True

        if DataValidator.isNotNull(self.form['mobile']):
            if (DataValidator.ismobilecheck(self.form['mobile'])):
                inputError['mobile'] = "Mobile No. should start with 6,7,8,9 and no. must be of 10 digits"
                self.form['error'] =  True    
             
        return self.form['error']

        

    def display(self, request, params={}):
        ContactListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list!=None:
            self.form['LastId'] = Contact.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'cityList':self.preloadData})
        return res

    def previous(self, request, params={}):
        ContactListCtl.count -= 1
        self.form['pageNo'] = ContactListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'cityList':self.preloadData})
        return res

    def next(self, request, params={}):
        ContactListCtl.count += 1
        self.form['pageNo'] = ContactListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Contact.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'cityList':self.preloadData})
        return res

    def submit(self, request, params={}):     
        ContactListCtl.count = 1
        record = self.get_service().search1(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found / Provide with correct value"
        ress = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'cityList':self.preloadData})
        return ress

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = ContactListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please select atleast one checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'cityList':self.preloadData})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if(id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']                        
                        if self.page_list!=None:
                            self.form['LastId'] = Contact.objects.last().id
                        ContactListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        print("ppppppppp----->>", self.page_list)
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'cityList':self.preloadData})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'cityList':self.preloadData})
        return res

    def get_template(self):
        return "ContactList.html"

    def get_service(self):
        return ContactService()
