import json
import os

class DMDataCustomization(object):
    def __init__(self, data_path, out_nlu):
        self.data_path = data_path
        self.out_nlu = out_nlu

    @staticmethod
    def dataRead(data):
        
        with open(data,'r') as data:
            mwoz_data = json.load(data)
            return mwoz_data
    
    @staticmethod
    def trainData(data_path, out_dm, C):
        greetings = ['general-welcome','general-thank','general-bye','general-reqmore']
        outliers = ['Train-Inform','Train-Request','Train-Select','Train-OfferBooked','Train-OfferBook','Taxi-Inform','Taxi-Request']

        with open(out_dm, "w") as f:
            pass

        data_access = DMDataCustomization.dataRead(data_path)

        def checkData(data, C):
            if isinstance(data, dict):
                data = getDictData(data, C)
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
                if dict_data is not None:
                    if c_R != 0 and  c_H == 0 and c_A == 0 and  c_T == 0 and c_P == 0 and c_HO == 0:
                        for utter_ind, utter_val in enumerate(dict_data):
                            entities = []
                            text_intent = []
                            user_intent = []
                            for items in utter_val:
                                if "text" in items:
                                    dialogue = utter_val[items]
                                    text = dialogue.lower()
                                if "intent" in items:
                                    int_ent = utter_val[items]
                                    for u_int in int_ent:
                                        if u_int in outliers:
                                            pass
                                        else:
                                            if "-" in u_int:
                                                u_int = u_int.replace("-","")
                                            user_intent.append(u_int)
                                    if len(user_intent) != 0:
                                        juser_intent = "".join(user_intent)
                                        
                                        if juser_intent is not None:
                                            if isinstance(int_ent,dict):
                                                for nest_entities in int_ent:
                                                    ent_val = int_ent[nest_entities]

                                                    if isinstance(ent_val, list):
                                                        for ent_pair in ent_val:
                                                            count = 1
                                                            for entity in ent_pair:
                                                                if count == 1:
                                                                    spec_entity = entity
                                                                if count == 2:
                                                                    spec_val = entity
                                                                count += 1
                                                            if spec_val in ['None','none'] or spec_val not in text:
                                                                text_intent.append({
                                                                    "text": dialogue,
                                                                    "intent": "{}".format(user_intent)
                                                                })
                                                            if spec_val in text:
                                                                entities.append(
                                                                    f"{spec_entity} : {spec_val}"
                                                                )

                                            with open(out_dm,'a') as f:
                                                if utter_ind % 2 == 0:                                                
                                                    if utter_ind == 0:
                                                        f.write("\n* Usergreetings\n")
                                                        f.write(" - generalsystemgreetings\n")
                                                    if juser_intent is not None:
                                                        f.write(f"* {juser_intent}{entities}")
                                                        f.write("\n")
                                                elif utter_ind % 2 == 1:
                                                    if len(entities)!=0:
                                                        f.write(f" - {juser_intent}{entities}")
                                                        f.write("\n")
                                                    elif len(text_intent)!=0:
                                                        f.write(f" - {juser_intent}")
                                                        f.write("\n")                           
                                            
        if isinstance(data_access,dict):
            print("json as a dict")
            for data in data_access:
                data = checkData(data_access[data], C)                     
        else:
            print("recheck")
