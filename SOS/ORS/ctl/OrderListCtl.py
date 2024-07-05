from ast import Try
from .BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from django.shortcuts import render
from service.forms import OrderForm
from service.models import Order
from service.service.OrderService import OrderService
# from service.service.ModelService import ModelService

class OrderListCtl(BaseCtl):
    count = 1
    def preload(self, request):
        self.page_list = [{'customer':'Rajat'},{'customer':'Jalaj'},{'customer':'Jitesh'},{'customer':'Aman'},{'customer':'Ajay'},{'customer':'Tarun'}]
        print("-----preload--self.page_list",self.page_list)
        self.preloadData = self.page_list

    def request_to_form(self, requestForm):
        self.form['productName'] = requestForm.get("productName", None)
        self.form['orderDate'] = requestForm.get("orderDate", None)
        self.form['quantity'] = requestForm.get("quantity", None)
        self.form['customer'] = requestForm.get("customer", None)
        self.form['ids'] = requestForm.get("ids", None)

    def input_validation(self):
        print("----input_validation------->>called")
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNotNull(self.form['productName']):
            if DataValidator.max_len_50(self.form['productName']):
                inputError['productName'] = "productName can only be of 50 Characters"
                self.form['error'] = True             
        
        if DataValidator.isNotNull(self.form['orderDate']):
            if DataValidator.isDate(self.form['orderDate']):
                inputError['orderDate'] = "orderDate should in past or present"
                self.form['error'] = True

        if DataValidator.isNotNull(self.form['quantity']):
            if (DataValidator.isnumb(self.form['quantity'])):
                inputError['quantity'] = "quantity should be in numbers"
                self.form['error'] =  True
            elif (DataValidator.not_0(self.form['quantity'])):
                inputError['quantity'] = "quantity cannot be 0"
                self.form['error'] =  True
            else:
                if DataValidator.max_len_20(self.form['quantity']):
                   inputError['quantity'] = "quantity should of 20 in length max"
                   self.form['error'] =  True   
             
        return self.form['error']

        

    def display(self, request, params={}):
        OrderListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if record['data']==None:
            self.form['LastId'] = Order.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'customerList':self.preloadData})
        return res

    def previous(self, request, params={}):
        OrderListCtl.count -= 1
        self.form['pageNo'] = OrderListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'customerList':self.preloadData})
        return res

    def next(self, request, params={}):
        OrderListCtl.count += 1
        self.form['pageNo'] = OrderListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Order.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'customerList':self.preloadData})
        return res

    def submit(self, request, params={}):     
        OrderListCtl.count = 1
        record = self.get_service().search1(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found / Provide with correct value"
        ress = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'customerList':self.preloadData})
        return ress

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = OrderListCtl.count
        if (bool(self.form['ids']) == False):
            print("qqqqqqqaaaaaaaaaaaqqqqqq------->>")
            self.form['error'] = True
            self.form['message'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'customerList':self.preloadData})
        else:
            print("qqqqqqqq--------------------->>")
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
                        if record['data']==None:
                            self.form['LastId'] = Order.objects.last().id
                        OrderListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'customerList':self.preloadData})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form,'customerList':self.preloadData})
        return res

    def get_template(self):
        return "OrderList.html"

    def get_service(self):
        return OrderService()
