from service.models import ShoppingCart
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains ShoppingCart business logics.   
'''

class ShoppingCartService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_shoppingcart where 1=1"
        val1 = params.get("name", None)
        val2 = params.get("product", None)
        val3 = params.get("date", None)
        val4 = params.get("quantity", None)
        
       
        print("-----val-->>",val1)
        if DataValidator.isNotNull(val1):
            sql += " and name = '"+val1+"' "
        if DataValidator.isNotNull(val2):
            sql += " and product = '"+val2+"'"
        if DataValidator.isNotNull(val3):
            sql += " and date = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " and quantity = '"+val4+"' "
        
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','name','product','date','quantity')
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            # print("--------with column-->>",{columnName[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>",params['MaxId'])
            res["data"].append({columnName[i]:  x[i] for i, _ in enumerate(x)})
        return res
    

    def get_model(self):
        return ShoppingCart
