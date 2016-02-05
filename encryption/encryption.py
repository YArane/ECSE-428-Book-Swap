'''
This file contains functions for encrypting and decrypting passwords using the RSA encryption algorithm
The objective is to encrypt passwords entered by users and store them into the account database
'''

import math
from fractions import gcd

# finds greatest common denominator for determining modular multiplicative inverse
def extended_gcd(a, b):
	
	remainder_prev, remainder = abs(a), abs(b)
	x, x_prev, y, y_prev = 0, 1, 1, 0
	
	while remainder:
		remainder_prev, (quotient, remainder) = remainder, divmod(remainder_prev, remainder)
		x, x_prev = x_prev - quotient * x, x
		y, y_prev = y_prev - quotient * y, y
	
	if a < 0:
		x_prev * -1
	if b < 0:
		y_prev * -1

	return remainder_prev, x_prev, y_prev

# returns the modular multiplicative inverse of a mod m
def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m

# finds reduced modulus a1 where 0 <= a < m and a = i % m
def reduced_mod(a, m):
	for i in range (0, m):
		if a == i % m:
			return i
	return a

# returns modulus: a^b % m
def find_mod(a, b, m):
	a1 = reduced_mod(a, m)
	p = 1
	for i in range (1, b + 1):
		p = p * a1
		p = reduced_mod(p, m)
	return p

# initializes elements for encryption/decryption
def initialize_elements():
	p = 11 # first prime
	q = 13 # second prime
	n = p * q # modulus
	t = (p - 1) * (q - 1) # totient

	e = 7 # public key
	
	# key is valid if greatest common factor between e and t is 1
	if gcd(e, t) != 1:
		print 'PUBLIC KEY IS INVALID'

	d = modinv(e, t) # key

	return p, q, n, t, e, d

# returns encrypted text
def encrypt(input):
	p, q, n, t, e, d = initialize_elements()
	output = ''

	for i in range (0, len(input)):
		m = ord(input[i])
		m = find_mod(m, e, n) % n # m^e % n
		output += chr(m)

	return output

# returns decrypted text
def decrypt(input):
	p, q, n, t, e, d = initialize_elements()
	output = ''

	for i in range (0, len(input)):
		c = ord(input[i])
		c = find_mod(c, d, n) % n # c^d % n
		output += chr(int(c))

	return output

# text = 'Hello World!'
# print '\nOriginal text:\n' + text + '\n'
#
# encrypted = encrypt(text)
# print 'Encrypted:\n' + encrypted + '\n'
#
# decrypted = decrypt(encrypted)
# print 'Decrypted:\n' + decrypted