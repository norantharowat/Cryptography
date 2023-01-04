import random
import pandas as pd

def xor_16bit_strings(x , delta_x): # to get x_double_dash

    result = ''
    for bit1, bit11 in zip(x, delta_x):
        if bit1 == "1" and bit11 == "1":
            result = result+ '0'
        elif bit1 == "0" and bit11 == "1":
            result = result+ '1'
        elif bit1 == "1" and bit11 == "0":
            result = result+ '1'
        else:
            result = result+ '0'
    return(result)

def generate_16bits():
   
    bits_16 = ""
 
    for i in range(16):
            
        temp = str(random.randint(0, 1))      
        bits_16 += temp
         
    return(bits_16)

def generate_pairs():
    first_plaintext =  generate_16bits()
    its_pair = xor_16bit_strings(first_plaintext , '0000010100000000')

    return(first_plaintext, its_pair)

def generate_10K_pairs():
    data_array = []
    # data = pd.DataFrame()
    for i in range(5000):
       first, second = generate_pairs() 
       result = [first, second]
       data_array.append(result)
    
    pd.DataFrame(data_array).to_pickle('plaintext_pairs.pkl')

generate_10K_pairs()

data = pd.read_pickle('./plaintext_pairs.pkl')

print(data)

