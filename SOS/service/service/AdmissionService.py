from service.models import Admission
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains User business logics.   
'''

class AdmissionService(BaseService):
    def authenticate(self, params={}):
        print("----auth--params-->",params)
        admissionList = self.search2(params)
        if (admissionList.count() == 1):
            print("----admissionList-0-index-->",admissionList[0])
            return admissionList[0]
        else:
            return None
        
    def search2(self, params):

        q = self.get_model().objects.filter()

        val = params.get("login_id", None)
        if(DataValidator.isNotNull(val)):
            q = q.filter(login_id=val)
            print("----q--->>",q)
        
        val = params.get("password", None)
        if(DataValidator.isNotNull(val)):
            q = q.filter(password=val)

        return q

    def search(self, params):
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("-------pageNo-->>",pageNo)
        sql = "select * from ORS_ADMISSION where 1=1"
        val1 = params.get("login_id", None)
        val2 = params.get("firstName", None)
        val3 = params.get("collageName", None)
        val4 = params.get("dob", None)

       
        print("-----val-->>",val1)
        if DataValidator.isNotNull(val1):
            sql += " and login_id = '"+val1+"' "
        if DataValidator.isNotNull(val2):
            sql += " and firstName like '"+val2+"%%'"
        if DataValidator.isNotNull(val3):
            sql += " and collageName = '"+val3+"' "
        if DataValidator.isNotNull(val4):
            sql += " and dob = '"+val4+"' "
        
            print("-------sql-->>",sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo']-1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "firstName", "lastName", "login_id", "password", "confirmpassword",
                      "dob", "address", "gender", "mobilenumber", "role_Id", "role_Name","collageName","parent_Names","parent_Contact_Number","parent_Occupations")
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
        return Admission 
