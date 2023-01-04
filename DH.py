import tinyec.ec as ec
import tinyec.registry as reg
import numpy as np
import timeit
""" First ECDH """
def ECDH():
    EC = reg.get_curve("secp256r1") # one of the standard EC in tinyec with prime p of 256 bits

    # EC_parameters = EC.g
    # print(EC_parameters)
    # print(EC.field)

    #y^2 = x^3 + 115792089210356248762697446949407573530086143415290314195533631308867097853948x + 41058363725152142129326129780047268409114441015993725554835256314039467401291

    p = 115792089210356248762697446949407573530086143415290314195533631308867097853951

    G = ec.Point(EC,48439561293906451759052585252797914202762949526041747995844080717082404635286,
    36134250956749795798585127919587881956611106672985015071877198253568414405109)

    # n is the order of the generator
    n = 115792089210356248762697446949407573529996955224135760322242422259061068512044369

    # pick na (Alice's private value)
    na = 8579208921035624876269744694940757352992695524413566031242422249061668517084901
    nb = 34752087218359948768697446949407573529996915224135760322242422259861068517043258

    pa = na * G
    pb = nb * G
    
    key_from_alice = na * pb
    key_from_bob = nb * pa

    print(key_from_alice == key_from_bob)
    time_ECDH = timeit.timeit(lambda: na * pb, number=100)

    return(time_ECDH)

import pyDH

Alice = pyDH.DiffieHellman(15)
Bob = pyDH.DiffieHellman(15)
Alice_pubkey = Alice.gen_public_key()
Bob_pubkey = Bob.gen_public_key()
Alice_sharedkey = Alice.gen_shared_key(Bob_pubkey)
Bob_sharedkey = Bob.gen_shared_key(Alice_pubkey)
print(Alice_sharedkey == Bob_sharedkey)

time_ECDH = ECDH()
time_DH = timeit.timeit(lambda:Alice.gen_shared_key(Bob_pubkey), number=100)

print(time_ECDH , time_DH)









