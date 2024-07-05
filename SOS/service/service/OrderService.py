from service.models import Order
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Order business logics.   
'''

class OrderService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_order where 1=1"
        
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnproductName = ('id','productName','orderDate','quantity','customer')
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            # print("--------with column-->>",{columnproductName[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>",params['MaxId'])
            res["data"].append({columnproductName[i]:  x[i] for i, _ in enumerate(x)})
        return res
    
    def search1(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_order where 1!=1"
        val1 = params.get("productName", None)
        val2 = params.get("orderDate", None)
        val3 = params.get("quantity", None)
        val4 = params.get("customer", None)
        
       
        print("-----val-->>",val1)
        if DataValidator.isNotNull(val1):             
            sql += " or productName like '"+val1+"%%' "
        if DataValidator.isNotNull(val2):
            sql += " or orderDate = '"+val2+"'"
        if DataValidator.isNotNull(val3):
            sql += " or quantity = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " or customer = '"+val4+"' "
        
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnproductName = ('id','productName','orderDate','quantity','customer')
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            # print("--------with column-->>",{columnproductName[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>",params['MaxId'])
            res["data"].append({columnproductName[i]:  x[i] for i, _ in enumerate(x)})
        return res
    

    def get_model(self):
        return Order
