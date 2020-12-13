import os
import numpy as np
import re
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

class decoderDataVectorization(object):
    def __init__(self, data):
        self.data = data    
          
    @staticmethod
    def extractData(data):
        try:
            de_inputs = []
            sen_len = []
            de_intent_sv, ind = {}, 1
            de_intent_sv['<pad>'] = 0
            full_en_data = []
            with open(data,'r') as in_data:
                for de_data in in_data:
                    if " -" in de_data:
                        de_i = de_data.replace(" - ","")
                        decoder_inputs = re.sub('[^a-zA-Z0-9: ''\n]', ' ', de_i)
                        full_de_data.append(decoder_inputs)
                        decoder_inputs = decoder_inputs.split()
                        sen_len.append(len(decoder_inputs))
                        for words in decoder_inputs:
                            if words not in de_inputs:
                                de_inputs.append(words)
            for index,val in enumerate(de_inputs):
                de_intent_sv[val] = index+1
            de_in_data = {index: token for token, index in de_intent_sv.items()}
            de_vocab_size = len(de_inputs)
            max_de_sen_len = max(sen_len)

            de_data = np.zeros((len(full_de_data), max_de_sen_len, de_vocab_size), dtype = 'float32')
            for i, in_text in enumerate(full_de_data):
                in_text = in_text.split()
                for t, word in enumerate(input_text):
                    de_data[i,t, de_intent_sv[word]] = 1.
                de_data[i, t + 1:, de_intent_sv[' ']] = 1.
                                         
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
    EDV = decoderDataVectorization(dp)
    EDV.extractData(dp)


