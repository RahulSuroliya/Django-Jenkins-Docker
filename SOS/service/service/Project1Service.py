from service.models import Project
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Project business logics.   
'''

class Project1Service(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_project where 1=1"
        
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnname = ('id','name','category','openDate','version')
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            # print("--------with column-->>",{columnname[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>",params['MaxId'])
            res["data"].append({columnname[i]:  x[i] for i, _ in enumerate(x)})
        return res
    
    def search1(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ors_project where 1!=1"
        val1 = params.get("name", None)
        val2 = params.get("category", None)
        val3 = params.get("openDate", None)
        val4 = params.get("version", None)
        
       
        print("-----val-->>",val1)
        if DataValidator.isNotNull(val1):             
            sql += " or name like '"+val1+"%%' "
        if DataValidator.isNotNull(val2):
            sql += " or category = '"+val2+"'"
        if DataValidator.isNotNull(val3):
            sql += " or openDate = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " or version = '"+val4+"' "
        
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnname = ('id','name','category','openDate','version')
        res = {
            "data":[]
         }
        count = 0
        for x in result:
            # print("--------with column-->>",{columnname[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>",params['MaxId'])
            res["data"].append({columnname[i]:  x[i] for i, _ in enumerate(x)})
        return res
    

    def get_model(self):
        return Project
