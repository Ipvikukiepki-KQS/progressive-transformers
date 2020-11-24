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
                
                if "text" in items:
                    dialogue = dict_data[items]
                    print("the text is", dialogue)
                
                if "intent" in items:
                    nest_intent = list(dict_data[items].keys())
                    print("the intent is", nest_intent)
                    print("intent entities are", dict_data[items])
                    int_ent = dict_data[items]
                    if isinstance(int_ent,dict):
                        for nest_entities in int_ent:
                            ent_val = int_ent[nest_entities]
                            print("entities are", ent_val)
                            if isinstance(ent_val, list):
                                for ent_pair in ent_val:
                                    print("the entities and values are", ent_pair)
                                    count = 1
                                    for entity in ent_pair:
                                        if count == 1:
                                            print("the entity is", entity)
                                        if count == 2:
                                            print("the value is", entity)
                                        count += 1
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