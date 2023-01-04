import hashlib
import hmac


def HMAC_SHA512(key, message):

    b = 1024

    opad = b'\x5c' * (b//8)
    ipad = b'\x36' * (b//8)

    if(len(key) <=  (b//8)):

        key_padded = key + b'\x00' * ((b//8) - len(key))
    else:
        return("Key size can not be larger than the output size of SHA-512")

   
    key_xor_ipad = bytes(key_padded[i] ^ ipad[i] for i in range(b//8))
    key_xor_opad = bytes(key_padded[i] ^ opad[i] for i in range(b//8))

    inner_hash = hashlib.sha512(key_xor_ipad)
    inner_hash.update(message) # Concat the message to the key_xor_ipad

    inner_hash_result = inner_hash.digest()

    outer_hash = hashlib.sha512(key_xor_opad)
    outer_hash.update(inner_hash_result) # Concat the inner_hash_result to the key_xor_opad

    HMAC = outer_hash.digest()

    return HMAC




key = b'This is my secrete key' 
message = b"I am using this input string to test my own implementation of HMAC-SHA-512."

my_HMAC = HMAC_SHA512(key, message)
print("HMAC my implementation: ", my_HMAC.hex())

library_HMAC = hmac.new(key ,message, digestmod = hashlib.sha512).digest()

print("HMAC from the library: " , library_HMAC.hex())

print(hmac.compare_digest(library_HMAC, my_HMAC))








    