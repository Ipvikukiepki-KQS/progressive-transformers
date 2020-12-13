import os
import numpy as np
import re
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

class EncoderDataVectorization(object):
    def __init__(self, data):
        self.data = data    
          
    @staticmethod
    def extractData(data):
        try:
            en_inputs = []
            sen_len = []
            en_intent_sv, ind = {}, 1
            en_intent_sv['<pad>'] = 0
            full_en_data = []
            with open(data,'r') as in_data:
                for en_data in in_data:
                    if "*" in en_data:
                        en_i = en_data.replace("* ","")
                        encoder_inputs = re.sub('[^a-zA-Z0-9: ''\n]', ' ', en_i)
                        full_en_data.append(encoder_inputs)
                        encoder_inputs = encoder_inputs.split()
                        sen_len.append(len(encoder_inputs))                       
                        for words in encoder_inputs:
                            if words not in en_inputs:
                                en_inputs.append(words)
                
            for index,val in enumerate(en_inputs):
                en_intent_sv[val] = index+1
            encoder_indata = {index: token for token, index in en_intent_sv.items()}
            en_vocab_size = len(en_inputs)
            max_en_sen_len = max(sen_len)
            
            en_data = np.zeros((len(full_en_data), max_en_sen_len, en_vocab_size), dtype = 'float32')
            for i, in_text in enumerate(full_en_data):
                in_text = in_text.split()
                for t, word in enumerate(input_text):
                    en_data[i,t, en_ti[word]] = 1.
                en_data[i, t + 1:, en_ti[' ']] = 1.

        except:
            if not os.path.exists(data):
                raise FileNotFoundError
            if os.path.isdir(data):
                print("A file has expected but a directory has provided. Please specify the train data file")                

if __name__ == '__main__':
    dp = os.path.relpath("traindata/DM_traindata.md")
    if os.path.exists(dp):
        pass
    else:
        raise FileNotFoundError
    EDV = EncoderDataVectorization(dp)
    EDV.extractData(dp)


