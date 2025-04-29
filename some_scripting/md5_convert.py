import hashlib
import sys

if len(sys.argv) != 2 or len(sys.argv) == 0:
    print ("How to use: python3 md5_convert.py \"example\"")
    exit()
else:
#txt = input("Enter a string to encode to MD5: ")
    txt = sys.argv[1]

    md5file = open("md5.txt", "a") 
    #with open("passwords.txt") as f:
    #    for word in f:
    word = hashlib.md5(txt.encode())
    md5 = word.hexdigest()
    md5file.write(md5 + "\n")

    md5file.close()