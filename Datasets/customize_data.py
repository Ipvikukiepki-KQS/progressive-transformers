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
    def trainData(data_path, out_nlu, C):
        print(data_path)
        data_access = DataCustomization.dataRead(data_path)        
        def checkData(data, C):
            if isinstance(data, dict):
                data = getDictData(data, C)
            elif isinstance(data, str):
                data = printStrData(data)
            return data

        def checkDictData(dict_data, C, c_R, c_H, c_A, c_T, c_P, c_HO):
            
            for items in dict_data:
                if "goal" in items:
                    nest_items = dict_data[items]
                    for elements in nest_items:
                        if "restaurant" in elements:
                            c_R = len(nest_items[elements])

                        if "hotel" in elements:
                            c_H = len(nest_items[elements])
                        
                        if "attraction" in elements:
                            c_A = len(nest_items[elements])
                        
                        if "taxi" in elements:
                            c_T = len(nest_items[elements])
                        
                        if "police" in elements:
                            c_P = len(nest_items[elements])
                        
                        if "hospital" in elements:
                            c_HO = len(nest_items[elements])
                if "log" in items:
                    dict_data = dict_data[items]
            return c_R, c_H, c_A, c_T, c_P, c_HO, dict_data

        def getDictData(dict_data, C):
            if C == 0:
                c_R, c_H, c_A, c_T, c_P, c_HO, dict_data = checkDictData(dict_data, C, c_R=0, c_H=0, c_A=0, c_T=0, c_P=0, c_HO=0)
                C = 1
            if C == 1 :
                if dict_data is not None and c_R != 0 and  c_H == 0 and c_A == 0 and  c_T == 0 and c_P == 0 and c_HO == 0:
                        #dict_data = getListData(dict_data, C)
                    if isinstance(dict_data,list):
                        dict_data = getListData(dict_data, C)
                    elif isinstance(dict_data,dict):
                        dict_data = dict_data
                    for items in dict_data:
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

        def getListData(list_data, C):

            for items in list_data:
                return items

        def printStrData(str_data):
            pass
            #print("The string is", str_data)
            
        if isinstance(data_access,dict):
            print("json as a dict")
            for data in data_access:
                data = checkData(data_access[data], C)                        
        else:
            print("recheck")

"""
        def checkDictData(dict_data):
            check_rest = 0
            check_hotel = 0
            check_attract = 0
            check_taxi = 0
            check_police = 0
            check_hospital = 0
            for items in dict_data:
                if "goal" in items:
                    nest_items = dict_data[items]
                    for elements in nest_items:
                        if "restaurant" in elements:
                            check_rest = len(nest_items[elements])

                        if "hotel" in elements:
                            check_hotel = len(nest_items[elements])
                        
                        if "attraction" in elements:
                            check_attract = len(nest_items[elements])
                        
                        if "taxi" in elements:
                            check_taxi = len(nest_items[elements])
                        
                        if "police" in elements:
                            check_police = len(nest_items[elements])
                        
                        if "hospital" in elements:
                            check_hospital = len(nest_items[elements])
            return check_rest, check_hotel, check_attract, check_taxi, check_police, check_hospital
        
        def getDictData(dict_data):
            for items in dict_data:
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
"""