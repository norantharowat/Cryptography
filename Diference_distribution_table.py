from collections import Counter
import pandas as pd
def xor_lists(A, B):
    result = []

    for (a,b) in zip(A,B): 

        result.append(a^b)
    return result

def s_box_mapping(input):
    S_box = {0: 12 ,1:7 ,2: 10,3:13,4:11,5:14,6:5,7: 1,
             8:3, 9:0,10:9,11:4,12:6,13:8,14:15,15:2}

    output = []
    for i in input:
        output.append(S_box[i])
    return output

def difference_distribution_table(delta_y):
    counts = [Counter(l) for l in delta_y ]

    table = []
    for count in counts:
        row = []
        for i in range(16):
            row.append(count[i])
        table.append(row)
    
    return pd.DataFrame(table)
    # return table


X = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
Y = s_box_mapping(X)
delta_x =  [[0]*16,[1]*16,[2]*16,[3]*16,[4]*16,[5]*16,[6]*16,[7]*16,
            [8]*16,[9]*16,[10]*16,[11]*16,[12]*16,[13]*16,[14]*16,[15]*16]

# X'' = X (xor) delta_x
x_double_dash = [xor_lists(X,d) for d in delta_x ]
y_double_dash = [s_box_mapping(l) for l in x_double_dash ]
delta_y = [xor_lists(Y,l) for l in y_double_dash ]


# print(difference_distribution_table(delta_y))
print(difference_distribution_table(delta_y).to_csv('difference_distribution_table.csv'))