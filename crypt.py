from cryptography.fernet import Fernet

key = "nelJ4yFu7AEWZvQWHv_1ce-EFQTOnNtDsCtLiT4GR5g="
fernet = Fernet(key)

# encrypt
if True:
	f = open("ai.py","rb")
	text = f.read()
	f.close()

	encrypted = fernet.encrypt(text)

	w = open("ai.md","wb")
	w.write(encrypted)
	w.close()

# decrypt
if True:
	f = open("ai.md","rb")
	text = f.read()
	f.close()

	decrypted = fernet.decrypt(text).decode("utf-8").replace("\r\n","\n")

	print(decrypted)