#https://pypi.python.org/pypi/enum34
#from enum import Enum

#class ResponseCode(Enum):
#    OK = 1
#	WARNING = 2
#	ERROR = 3

class ResponseMessage:
    
    def __init__(self, errorCode, errorMessage):
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        
    def getErrorCode(self):
        return self.errorCode