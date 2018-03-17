import sys,os
import hashlib, uuid
import getpass



def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]

def getInt(p=''):
	output=0
	for x in p:
		output+=ord(x)
	return output

def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

def rotate(l, n):
    return l[n:] + l[:n]


def encrypt(file,n=0):
	f = open(file)
	data = ""
	for line in f:
		data = data + line
	lenData=len(data)
	if data[lenData-1]=='0' or data[lenData-1]=='1':
		return False
	list = string2bits(data)
	list.append("00000001")
	l = len(list)
	n=n%l
	list = rotate(list,n)
	encData = ''.join(list)
	temp = sys.stdout
	sys.stdout = open(file,'w')
	sys.stdout.write(encData)
	sys.stdout = temp
	return True

def decrypt(file,n=0):
	f = open(file)
	data = ""
	for line in f:
		data = data + line
	lenData=len(data)
	if data[lenData-1]!='0' and data[lenData-1]!='1':
		return False
	list = [data[i:i+8] for i in range(0, len(data), 8)]
	l = len(list)
	n=n%l
	list = rotate(list,l-n)
	list.pop()
	decData = bits2string(list)
	temp = sys.stdout
	sys.stdout = open(file,'w')
	sys.stdout.write(decData)
	sys.stdout = temp
	return True

def validate(password):
	salt = "395fb70b393b42c58f98d172b97fc759" #uuid.uuid4().hex
	hashed_password = hashlib.sha512(password + salt).hexdigest()
	if hashed_password=="8affa51aadaf8cc5d0dd78d9b8eae59221e5c0db55f3e7c7800f41c366be86afeb6f14fa0faede86a65b5614e13820c53164aade796c5892c17c781115332276":
		return True
	else:
		return False

def processfile(file,n):
	if sys.argv[2]=="e":
		if encrypt(file,n):
			print(file+" encrypted succesfully")
		else:
			print(file+" seems to be already encrypted")
	if sys.argv[2]=="d":
		if decrypt(file,n):
			print(file+" decrypted succesfully")
		else:
			print(file+" seems to be already decrypted")

def processdir(path,n):
	for file_or_dir in os.listdir(path):
		file_or_dir = os.path.join(path, file_or_dir)
		if os.path.isdir(file_or_dir):
			processdir(file_or_dir,n)
		if os.path.isfile(file_or_dir):
			processfile(file_or_dir,n)

password = getpass.getpass()
if validate(password):
	if len(sys.argv)<3:
		print("Expected 2 arguments")
		exit()
	n = getInt(password)
	if os.path.isfile(sys.argv[1]):
		processfile(sys.argv[1],n)
		exit()
	if os.path.isdir(sys.argv[1]):
		path = sys.argv[1]
		processdir(sys.argv[1],n)
		exit()
	print("Wrong file/dir path")
else:
	print("Wrong Password!")




