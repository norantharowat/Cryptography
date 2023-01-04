import numpy as np
def Miller_Rabin_test(n): # n is odd number
    # because n is odd number we have ---> n - 1 = 2^k * q 
    
    # (1) First, we need to find k and q such that k > 0 and q odd number

    q = n - 1 # start with the highest possible value of q which is n -1
    k = 0     # start with lowest possible value of k which is 0

    while ((q % 2) == 0): # as long as q is an even number do the following
        k += 1 # keep increasing k
        q = q//2 # q/2 with result of type Integer, keep reducing q until we reach an odd number
        

    # (2) Now we choose a random integer 'a' between 1 and n-1 --> 1 < a < n - 1
    a = np.random.randint(2 , n - 1)

    # (3) check if a^q mod n is equal to 1 or not, if so return inclusive

    if ( ( a ** q ) % n == 1) :
        return True

    # (4) check powers of a for  0 <= j <= k -1
    # if a^(2^j * q) mod n = n-1 return inconclusive

    for j in range(k):
        
        exp = (2 ** j) * q


        if ((a ** exp) % n == (n - 1)):
           
            return True

    return False # if the two ptoperties failed return composite, retun false it is not a prime

# for t = 5
# number = 53
t = 5
def result(n):
    is_prime = True
    for i in range(t):
        if not Miller_Rabin_test(n):
            print("The number "+ str(n) + " is composite with confidence t = 5")
            is_prime = False
            break

    if is_prime:
        print("The number "+ str(n) + " is probably prime with confidence t = 5")

    return is_prime

# let us try 14 bit numbers between 13750 , 13850 to see the probably prime numbers in this range

primes = []
for i in range(13750, 13851):
    is_prime = result(i)

    if(is_prime):
        primes.append(i)
print(primes)