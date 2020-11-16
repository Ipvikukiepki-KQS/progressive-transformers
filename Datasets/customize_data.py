import json
import os

class DataCustomization(object):
    def __init__(self, data_path, out_nlu):
        self.data_path = data_path
        self.out_nlu = out_nlu

    @staticmethod
    def dataRead(data):
        
        with open(data,'r') as data:
            sgd_data = json.load(data)
            return sgd_data
    
    @staticmethod
    def trainData(data_path, out_nlu):
        print(data_path)
        keys = []
        data_access = DataCustomization.dataRead(data_path)
        if isinstance(data_access,list):
            print("json as a list")
            for data in data_access:
                if isinstance(data,dict):
                    for items in data:
                        if isinstance(data[items],str):
                            print("dict items are strings")
                        elif isinstance(data[items],list):
                            print("dict tems are lists")
                        else:
                            print("dict items are dict")

                        
    
        else:
            print("recheck")
            