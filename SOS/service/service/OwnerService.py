from service.models import Owner
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Owner business logics.   
'''

class OwnerService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_owner where 1=1"
        
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnproductName = ('id','name','dob','vehicleId','insuranceAmount')
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
        sql = "select * from ors_owner where 1!=1"
        val1 = params.get("name", None)
        val2 = params.get("dob", None)
        val3 = params.get("vehicleId", None)
        val4 = params.get("insuranceAmount", None)
        
       
        print("-----val-->>",val1)
        if DataValidator.isNotNull(val1):             
            sql += " or name like '"+val1+"%%' "
        if DataValidator.isNotNull(val2):
            sql += " or dob = '"+val2+"'"
        if DataValidator.isNotNull(val3):
            sql += " or vehicleId = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " or insuranceAmount = '"+val4+"' "
        
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnproductName = ('id','name','dob','vehicleId','insuranceAmount')
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
        return Owner
