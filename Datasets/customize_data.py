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

        def checkData(data):
            if isinstance(data, dict):
                data = printDictData(data)
            elif isinstance(data, list):
                data = printListData(data)
            elif isinstance(data, str):
                data = printStrData(data)
            return data

        def printDictData(dict_data):
            for items in dict_data:
                if "goal" in items:
                    nest_items = dict_data[items]
                    for elements in nest_items:
                        if "restaurant" in elements:
                            check_rest = len(nest_items[elements])
                            #print("length is", check_rest)
                        if "hotel" in elements:
                            check_hotel = len(nest_items[elements])
                            #print("length is", check_hotel)
                        if "attraction" in elements:
                            check_attract = len(nest_items[elements])
                            #print("length is", check_attract)
                
                if "log" in items:
                    nest_dict = dict_data[items]
                    for elements in nest_dict:
                        pass
                else:
                    checkData(dict_data[items])    
        def printListData(list_data):
            for items in list_data:
                checkData(items)
        def printStrData(str_data):
            print("The string is", str_data)
            
        if isinstance(data_access,dict):
            print("json as a dict")
            for data in data_access:
                data = checkData(data_access[data])                        
        else:
            print("recheck")


"""
                    nest_items = dict_data[items]
                    for elements in nest_items:
                        if "restaurant" in elements:
                            check_rest = len(nest_items[elements])
                            print("length is", check_rest)
                        if "hotel" in elements:
                            check_hotel = len(nest_items[elements])
                            print("length is", check_hotel)
                        if "attraction" in elements:
                            check_attract = len(nest_items[elements])
                            print("length is", check_attract)
                
                if "log" in items:
                    nest_dict = dict_data[items]
                    for elements in nest_dict:
                        print(elements)   """               
