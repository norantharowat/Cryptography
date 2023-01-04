import pandas as pd

data = pd.read_pickle('./plaintext_pairs.pkl')

# for idx, row in data.iterrows():
#     print([row[0], row[1]])

def s_box_mapping(input):
    S_box = {'0000': '1100' ,'0001':'0111' ,'0010': '1010', '0011':'1101', '0100':'1011', '0101':'1110', '0110':'0101', '0111':'0001',
             '1000':'0011', '1001':'0000','1010':'1001','1011':'0100','1100':'0110','1101':'1000','1110':'1111','1111':'0010'}

   
    return S_box[input]

def permutation(bits):

    mapping =  {0: 0 ,1:4 ,2: 8,3:12,4:1,5:5,6:9,7: 13,
             8:2, 9:6,10:10,11:14,12:3,13:7,14:11,15:15}

    result = ['0']*16

    for i in range(16):
        bit = bits[i]
        new_pos = mapping[i]

        result[new_pos] = str(bit)

    return("".join(result))

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

round_keys = ['1010000001000110' , '0101100010000101', '1111111000111100 ', '1010111110111110', '0010101001001001']

def SPN( plaintext):  # 16 bits

    first_four = round_keys[0:4]
    output = ''
    for k in first_four:
        
        input_to_sbox = xor_16bit_strings(plaintext , k)

        output_of_sbox = s_box_mapping(input_to_sbox[0:4]) + s_box_mapping(input_to_sbox[4:8]) + s_box_mapping(input_to_sbox[8:12]) + s_box_mapping(input_to_sbox[12:16])

        if ( k == '1010111110111110'): # if we reach R - 1 no permutation
            output = output_of_sbox
        else:
            output = permutation(output_of_sbox)

        

    cipher = xor_16bit_strings(output , round_keys[4]) 

    return(cipher)

def encrypt_pairs():
    data_array = []
    for idx, row in data.iterrows():

        first, second = SPN( row[0]) , SPN( row[1])
        result = [first, second]
        data_array.append(result)
        

    print(pd.DataFrame(data_array))
    pd.DataFrame(data_array).to_pickle('ciphertext_pairs.pkl')        
        
encrypt_pairs()
# print(SPN('0101010011000011'))
# print(permutation('0101010011000011'))
