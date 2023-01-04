import numpy as np

q = 89 # q is a prime number

alpha = 13 # alpha is a primitive root of q

M = np.random.randint(0, q ) #  0 <= M <= q - 1
# M = 56
# M = 33

def key_generation_by_userA():

    X_A = np.random.randint(2, q - 1) # 1 < X_A < q-1
    # X_A = 21 # 1 < X_A < q-1

    Y_A = (alpha**X_A) % (q) # Public key of user A is {q, alpha, Y_A}

    return(X_A , Y_A)


def Encryptio_by_userB_with_userA_PublicKey(Y_A, k, message):
   
    #k = np.random.randint(1, q ) # 1 <= k <= q-1

    one_time_key_K = (Y_A**k) % (q)  # One time key K = (YA)^k mod q

    # Encrypt M as pair of integers ( C1, C2 )
    
    C1 = (alpha**k) % (q) # C1 = (alpha)^k mod q

    C2 = (one_time_key_K * message) % (q) # C2 = KM mod q

    cipher_text = {'C1': C1 , 'C2':C2}

    return cipher_text

def Decryption_by_userA_with_userA_Private_Key(A_private_key,cipher_text):
    
    one_time_key_K = (cipher_text['C1']**A_private_key) % (q)  # One time key K =  (C1) ^ X_A mod q

    K_inverse = pow(one_time_key_K, q-2, q) # To get the multiplicative inverse of the one_time_key_K

    plaintext = (cipher_text['C2'] * K_inverse) % (q) # Get the plaintext

    return plaintext


print("Plaintext M = " + str(M) + " , prime number q = " + str(q) + " , alpha = " + str(alpha))
A_private_key , A_public_key = key_generation_by_userA()

print("Private key of user A = " + str(A_private_key) + ", Public key of user A = " + str(A_public_key))

k = np.random.randint(1, q ) # 1 <= k <= q-1
# k = 37
cipher_text = Encryptio_by_userB_with_userA_PublicKey(A_public_key , k , M)

print("Cipher text encrypted by userB is = " + str(cipher_text))

decrypted_M = Decryption_by_userA_with_userA_Private_Key(A_private_key,cipher_text)

print("The message after decryption by userA is = " + str(decrypted_M))