"""
Code inspired by this repository: https://github.com/Amaterazu7/rsa-python/blob/master/rsa.py
"""

import random
from modint import chinese_remainder
import timeit
'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
from Crypto.Util import number

# p = number.getPrime(1024)
# q = number.getPrime(1024)

# print("p 1024 prime number: " , p )
# print("----------------------------")
# print("q 1024 prime number: " , q )

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi



def generate_key_pair(p, q):
  
    n = p * q
   
    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    # e = random.randrange(1, phi)
    e = 65537

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private key_pair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    # cipher = [pow(ord(char), key, n) for char in plaintext]
    cipher = pow(plaintext, key, n) 
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    # aux = [str(pow(char, key, n)) for char in ciphertext]
    plain = pow(ciphertext, key, n)
    # Return the array of bytes as a string
    # plain = [chr(int(char2)) for char2 in aux]
    
    return plain


def decrypt_with_CRT(pk, ciphertext , p ,q):
    # Unpack the key into its components
    key, n = pk
    #prime factors of n are p and , q
    phi_p , phi_q = (p-1) , (q-1)
    k_tuple_base = [ciphertext % p , ciphertext % q]
    k_tuble_exponent = [key % phi_p, key % phi_q]
    combined_k_tuple = [pow(k_tuple_base[0], k_tuble_exponent[0], p) , 
                        pow(k_tuple_base[1], k_tuble_exponent[1], q)] 

    plain = chinese_remainder([p,q],combined_k_tuple)
   
    return plain


if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print("===========================================================================================================")
    print("================================== RSA Encryptor / Decrypter ==============================================")
    print(" ")

    p = 91751366669166074120541722524720893912559835689205600622680061479959894085917135161895937387227578168027075450099564925280206853923601226692025053892697755202455744825040594726661800414786567902830018446125357855447230934799635096072019075404125038964831673056835628302194251930646259258459572389940924345671

    q = 100292089968762125238599067031791290167971357955258227091111705217523020287092003799449727003178658205360026400841754183892568839822238201369750001780535569064968169611357441060345690066888321065431961305725336436816527933199483147655851571536135410800222793645862646521527529741033027583494435042663940785181
    # print(p %2 , q%2)

    print(" - Generating your public / private key-pairs now . . .")

    public, private = generate_key_pair(p, q)

    print(" - Your public key is ", public, " and your private key is ", private)

    message = 466921883457309
    encrypted_msg = encrypt(public, message)

    print(" - Your encrypted message is: ", encrypted_msg)
    print(" - Decrypting message with private key ", private, " . . .")
    # print(" - Your message is: ", decrypt(private, encrypted_msg))
    print(" - Your message is: ", decrypt_with_CRT(private, encrypted_msg , p ,q))

    dec_without_crt = timeit.timeit(lambda: decrypt(private, encrypted_msg), number=100)
    dec_with_crt = timeit.timeit(lambda: decrypt_with_CRT(private, encrypted_msg , p ,q), number=100)
    print("Time in seconds to decrypt without CRT ", dec_without_crt )
    print("Time in seconds to decrypt with CRT ", dec_with_crt)

    # print(" ")
    # print("============================================ END ==========================================================")
    # print("===========================================================================================================")