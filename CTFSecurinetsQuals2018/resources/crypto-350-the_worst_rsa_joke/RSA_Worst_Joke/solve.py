#!/usr/bin/env python
 
#####################################################################
#SOURCE : https://gist.github.com/tylerl/1239116
#####################################################################
#We edited this python file from this gist page and we adapted it to the task
#Because the built-in classes does not support a custom private key with a single prime
 
 
# This example demonstrates RSA public-key cryptography in an
# easy-to-follow manner. It works on integers alone, and uses much smaller numbers
# for the sake of clarity.
 
from Crypto.PublicKey import RSA
import sys
import base64
 
#Public key
pub_str = """-----BEGIN PUBLIC KEY-----                                                      
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEBITsFfW/evEUntbdCGsHp                
PM/+p2xPCHSZHPP6zw6rnvZGohg5ggtNZTqRa2jyWOnT98K6BU5K8F8+TWGz3nct                
KtIziw6ubqCPIHbk5LCKsgkg+miF5sRN7BvuKKh2U8dLy56fEpTeiki9YUZSo9ZZ                
3857iURhDyW/r5NumlQWfE0ifRbTLmXqRYtp1g3s1/oDTBs72GJxcWTneF6wbcxb                
iLqiYuQxIOVGZcDLyz6tUbCgCBm06R1IctP753JOA6txvK+LuEx03slqrfyxhlOo                
8FOT1mYGmSO8e5sxNj1tbZtFn0bbW6+W+EBKrxqDHw24qtfZOkJW6BVrK3B1egEg                
kwIDAQAB                                                                        
-----END PUBLIC KEY-----
"""
 
ciphertext=open("flag.enc","r").read()
 
pub=RSA.importKey(pub_str)
 
MOD=pub.n
#MOD=3651197469459369027264435486453493420052204562318775238482359472927573078919168051490502708495072951414867950700505804714603186999576876503487649
# MOD Is Not : MOD=P*Q
 
P=MOD
#Q= # Second prime Not picked
E=pub.e
#E=65537# usually a constant; 0x10001 is common, prime is best
 
 
#####################################################################
# Next, some functions we'll need in a moment:
#####################################################################
# Note on what these operators do:
# %  is the modulus (remainder) operator: 10 % 3 is 1
# // is integer (round-down) division: 10 // 3 is 3
# ** is exponent (2**3 is 2 to the 3rd power)
 
# Brute-force (i.e. try every possibility) primality test.
def isPrime(x):
    if x%2==0 and x>2: return False     # False for all even numbers
    i=3                                 # we don't divide by 1 or 2
    sqrt=x**.5                          
    while i<sqrt:
        if x%i==0: return False
        i+=2
    return True
 
def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.
 
   Unless b==0, the result will have the same sign as b (so that when
   b is divided by it, the result comes out positive).
   """
    while b:
        a, b = b, a%b
    return a
 
# Part of find_inverse below
# See: http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def eea(a,b):
    if b==0:return (1,0)
    (q,r) = (a//b,a%b)
    (s,t) = eea(b,r)
    return (t, s-(q*t) )
 
# Find the multiplicative inverse of x (mod y)
# see: http://en.wikipedia.org/wiki/Modular_multiplicative_inverse
def find_inverse(x,y):
    inv = eea(x,y)[0]
    if inv < 1: inv += y #we only want positive values
    return inv
 
def text2Int(text):
    """Convert a text string into an integer"""
    return reduce(lambda x, y : (x << 8) + y, map(ord, text))
 
def int2Text(number, size):
    """Convert an integer into a text string"""
    text = "".join([chr((number >> j) & 0xff) for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")
 
#####################################################################
# Make sure the numbers we picked above are valid.
#####################################################################
 
# Not : T=(P-1)*(Q-1)
T=(P-1) # Euler's totient (intermediate result)
 
# Assuming E is prime, we just have to check against T
if E<1 or E > T: raise Exception("E must be > 1 and < T")
if gcd(E,T)!=1: raise Exception("E is not coprime with T")
 
#####################################################################
# Now that we've validated our random numbers, we derive our keys.
#####################################################################
 
# Private exponent is inverse of public exponent with respect to (mod T)
D = find_inverse(E,T)
 
# The modulus is always needed, while either E or D is the exponent, depending on
# which key we're using. D is much harder for an adversary to derive, so we call
# that one the "private" key.
 
print "public key: (MOD: %i, E: %i)" % (MOD,E)
print "private key: (MOD: %i, D: %i)" % (MOD,D)
 
# Note that P, Q, and T can now be discarded, but they're usually
# kept around so that a more efficient encryption algorithm can be used.
# http://en.wikipedia.org/wiki/RSA#Using_the_Chinese_remainder_algorithm
 
#####################################################################
# We have our keys, let's do some encryption
#####################################################################
 
# Here I only focus on whether you're applying the private key or
# applying the public key, since either one will reverse the other.
 
def encrypt_or_decrypt(line, MOD, key):
    try: before=int(line)
    except ValueError:
        print "not a number: \"%s\"" % (line)
 
    if before >= MOD:
        print "Only values up to %i can be encoded with this key (choose bigger primes next time)" % (MOD,)
 
    # Note that the pow() built-in does modulo exponentation. That's handy, since it saves us having to
    # implement that ablity.
    # http://en.wikipedia.org/wiki/Modular_exponentiation
 
    after = pow(before,key,MOD) #encrypt/decrypt using this ONE command. Surprisingly simple.
    return after
 
# Decryption with the private key
plaintext2=int2Text(encrypt_or_decrypt(text2Int(base64.b64decode(ciphertext)),MOD,D),1024)
print "Plaintext (from base64):",plaintext2
