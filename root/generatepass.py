
import hashlib 
from hashlib import *

username = 'admin'
password = 'password'
combo = username+','+password
priv = '1'
hashedcombo = hashlib.sha3_512(combo.encode('utf-8')).hexdigest()

file = open('login.txt', 'a')
file.write(hashedcombo + priv + "\n" )
file.close()





