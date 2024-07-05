from service.models import Car
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Car business logics.   
'''

class CarService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_car where 1=1"
        val1 = params.get("carId", None)
        val2 = params.get("brand", None)
        val3 = params.get("model", None)
        val4 = params.get("price", None)
       
        print("-----val-->>",val1)
        if DataValidator.isNotNull(val1):
            sql += " and carId = '"+val1+"' "
        if DataValidator.isNotNull(val2):
            sql += " and brand like '"+val2+"%%'"
        if DataValidator.isNotNull(val3):
            sql += " and model = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " and price = '"+val4+"' "
        
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','carId','brand','model','dateOfMenufactoring','price')
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
        return Car
