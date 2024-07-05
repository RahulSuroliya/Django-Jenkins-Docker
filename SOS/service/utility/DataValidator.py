from datetime import *
import re
from types import ClassMethodDescriptorType
class DataValidator:

    

    @classmethod
    def isInt(self, val):
        if(val == 0):
            return False
        else:
            return True
            
    @classmethod
    def ismobilecheck(self, val):
        if re.match("^[6-9]\d{9}$", val):
            return False
        else:
            return True
        
    @classmethod
    def isNotNull(self, val):
        if(val == None or val == ""):
            return False
        else:
            return True

    @classmethod
    def isNull(self, val):
        if(val == None or val == ""):
            return True
        else:
            return False

    @classmethod
    def isDate(self, val):
        if re.match("([0-2]\d{3})-(0\d|1[0-2])-([0-2]\d|3[01])", val):
            if(datetime.strptime(val,"%Y-%m-%d") <= datetime.strptime(str(date.today()),"%Y-%m-%d")):# Comparing date with current date
                return False
            else:
                return True
        else:
            return True

    @classmethod
    def ischeck(self, val):
        if(val == None or val == ""):
            return True
        else:
            if(0 <= int(val) <= 100):
                return False
            else:
                return True

    @classmethod
    def ischeckroll(self, val):
        if re.match("^(?=.*[0-9]$)(?=.*[A-Z])", val):
            return False
        else:
            return True


    @classmethod
    def isalphacheck(self, val):
        if re.match("^[a-zA-z\s]+$", val):
            return False
        else:
            return True

    @classmethod
    def ismobilecheck(self, val):
        if re.match("^[6-9]\d{9}$", val):
            return False
        else:
            return True


    @classmethod
    def isemail(self, val):
        if re.match("[^@]+@[^@]+\.[^@]+", val):
            return False
        else:
            return True


    @classmethod
    def isphonecheck(self, val):
        if re.match("^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$", val):
            return False
        else:
            return True
        
    @classmethod
    def isnumb(self, val):
        if val.isnumeric()==True:
            return False
        else:
            return True
        
    @classmethod
    def max_len_50(self,val):
        if len(str(val)) <= 50:
            return False
        else:
            return True
        
    @classmethod
    def max_len_20(self,val):
        if len(str(val)) <= 20:
            return False
        else:
            return True
        
    @classmethod
    def max_len_100(self,val):
        if len(str(val)) <= 100:
            return False
        else:
            return True
        
    @classmethod
    def not_0(self,val):
        if val != 0:
            return False
        else:
            return True