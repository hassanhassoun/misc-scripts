import os,binascii


for i in range ( 1, 19 ):
   print "          '#" + binascii.b2a_hex(os.urandom(3)) + "',"
