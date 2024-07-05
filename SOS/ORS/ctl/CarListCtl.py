from ast import Try
from .BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from django.shortcuts import render
from service.forms import CarForm
from service.models import Car
from service.service.CarService import CarService
# from service.service.ModelService import ModelService

class CarListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        self.page_list = CarService().preload()
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        self.form['carId'] = requestForm.get("carId", None)
        self.form['brand'] = requestForm.get("brand", None)
        self.form['model'] = requestForm.get("model", None)
        self.form['dateOfMenufactoring'] = requestForm.get("dateOfMenufactoring", None)
        self.form['price'] = requestForm.get("price", None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        CarListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Car.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def previous(self, request, params={}):
        CarListCtl.count -= 1
        self.form['pageNo'] = CarListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def next(self, request, params={}):
        CarListCtl.count += 1
        self.form['pageNo'] = CarListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Car.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def submit(self, request, params={}):
        CarListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found"
        ress = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return ress

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = CarListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please select atleast one checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
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
                        self.form['LastId'] = Car.objects.last().id
                        CarListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        print("ppppppppp----->>", self.page_list)
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def get_template(self):
        return "CarList.html"

    def get_service(self):
        return CarService()
