from cryptography.fernet import Fernet
import os

key = os.environ['FERNET']
fernet = Fernet(key)

files = ["service","Clock","Bot","Agent","Trader","Strategy","Strategies"]

# decrypting
if True:
	print("Loading crypted files...")
	for i in files:
		f = open(f"{i}.enc","rb")
		text = f.read()
		f.close()
		f = open(f"{i}.py","wb")
		f.write(fernet.decrypt(text))
		f.close()
	print("Files decrypted.")

# decrypting
# print("Loading crypted model...")
# f = open("cmodel.pkl","rb")
# text = f.read()
# f.close()
# f = open("model.pkl","wb")
# f.write(fernet.decrypt(text))
# f.close()
# print("Model decrypted.")
