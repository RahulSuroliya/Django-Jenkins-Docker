from service.models import Patient
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Contact business logics.   
'''

class PatientService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_patient where 1=1"
        
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','name','dov','mobile','decease')
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
    
    def search1(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_patient where 1!=1"
        val1 = params.get("name", None)
        val2 = params.get("decease", None)
        val3 = params.get("dov", None)
        val4 = params.get("mobile", None)
        
       
        print("-----val-->>",val1)
        if DataValidator.isNotNull(val1):             
            sql += " or name = '"+val1+"' "
        if DataValidator.isNotNull(val2):
            sql += " or decease = '"+val2+"'"
        if DataValidator.isNotNull(val3):
            sql += " or dov = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " or mobile = '"+val4+"' "
        
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','name','dov','mobile','decease')
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
        return Patient
