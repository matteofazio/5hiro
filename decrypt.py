from cryptography.fernet import Fernet

key = os.environ['FERNET']
fernet = Fernet(key)

# decrypting
f = open("cmodel.pkl","rb")
text = f.read()
f.close()
f = open("model.pkl","wb")
f.write(fernet.decrypt(text))
f.close()