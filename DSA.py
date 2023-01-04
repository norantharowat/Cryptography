from Crypto.PublicKey import DSA
import numpy as np
from Crypto.Util import number
import random 
import hashlib


key = DSA.generate(1024)

p = key.domain()[0]
q = key.domain()[1]
# g = key.domain()[2]

# g = h^(p-1) /q mod p and h is any integer between 1 and (p-1)
expo = (p - 1) // q
g = pow(12556454651321, expo, p)

print("p 1024 prime is = " , p)
print("q 160 prime is = " , q)
print("g generator of the subgroup z_p* = " , g)
print("check q divides (p - 1): " , (p - 1) % q == 0)
print("size of p is : " , len(bin(p)) -2 )
print("size of q is : " , len(bin(q)) -2)
print("size of g is : " , len(bin(g)) -2)


Alice_private_key = random.randrange(1, q-1)
Alice_public_key = pow(g, Alice_private_key, p)

print("Alice's private key: ", Alice_private_key)

def sign(m):

    k = random.randrange(1, q-1)
    K_inverse = pow(k, q-2, q)

    m_hash = hashlib.sha1(str(m).encode('ASCII')).hexdigest()

    r = (pow(g, k, p)) % q

    S = (K_inverse * ( int(m_hash, 16) + Alice_private_key * r)) % q

    signature = (r, S)

    return (signature , k)

def verify(signature , m ):

    r , s = signature
    m_hash = hashlib.sha1(str(m).encode('ASCII')).hexdigest()

    w = pow(s, q-2, q)
    u1 = (int(m_hash, 16) * w ) % q
    u2 = (r * w) % q

    v = ((pow(g, u1, p) * pow(Alice_public_key, u2, p)) % p ) % q

    print("signature is : " , signature)
    print("v is : " , v)

    if(v == r):
        return("signature is valid on the message")

    else:
        return("signature is not valid on the message")

def sign_with_same_k(m,k):

    K_inverse = pow(k, q-2, q)

    m_hash = hashlib.sha1(str(m).encode('ASCII')).hexdigest()

    r = (pow(g, k, p)) % q

    S = (K_inverse * ( int(m_hash, 16) + Alice_private_key * r)) % q

    signature = (r, S)

    return signature 

def compromise(signature1, signature2, m1, m2):

    m1_hash = hashlib.sha1(str(m1).encode('ASCII')).hexdigest()
    m2_hash = hashlib.sha1(str(m2).encode('ASCII')).hexdigest()
    S_diff_inverse = pow((signature1[1] - signature2[1]), q-2, q)

    # k = ((m1_hash - m2_hash) / (signature1[1] - signature2[1])) % q
    k = ((int(m1_hash, 16) - int(m2_hash, 16)) * S_diff_inverse ) % q
    print("K derived: ", k)

    get_Alice_private_key = ((k * signature1[1] - int(m1_hash, 16) ) * pow(signature1[0] , q-2, q) ) % q
    print("Derived Alic's private key: ", get_Alice_private_key)


m = 522346828557612
m2 = 8161474912883

signature , k = sign(m)
print("K", k)
signature2 = sign_with_same_k(m2,k)

print(verify(signature , m ))
print(verify(signature2 , m2 ))

compromise(signature, signature2, m, m2)

