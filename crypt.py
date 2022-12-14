from cryptography.fernet import Fernet
from xgboost import XGBClassifier

key = "-xOsNOG1iDx-Tsn1Mb5u41NtEZ4CwcaN-7ipebvdipg="
fernet = Fernet(key)

# encrypt
if True:
	f = open("_model.json","rb")
	text = f.read()
	f.close()

	encrypted = fernet.encrypt(text)

	w = open("cmodel.json","wb")
	w.write(encrypted)
	w.close()

# decrypt
if True:
	f = open("cmodel.json","rb")
	text = f.read()
	f.close()
	f = open("model.json","wb")
	f.write(fernet.decrypt(text))
	f.close()
	model = XGBClassifier()
	model.load_model("model.json")
	print(model._Booster)