import argparse
import os
import getpass
from datetime import date
from datetime import datetime
from cryptography.fernet import Fernet
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

parser = argparse.ArgumentParser(prog = 'Journal_App', description = 'Perosnal Journal Management');


def readJournalOrCreateJournal(isRead, globalUser):
	if(isRead == "1"):
		readJornal(globalUser)
		print("Wish to Continue ? ")
		inp = input("Hit 1 to Read OR 2 for New Record OR 3 to Upload OR E for EXIT: ")
		readJournalOrCreateJournal(inp, globalUser)
	elif(isRead == "2"):
		newJournal(globalUser)
		print("Wish to Continue ? ")
		inp = input("Hit 1 to Read OR 2 for New Record OR 3 to Upload: ")
		readJournalOrCreateJournal(inp, globalUser)
	elif(isRead == "3"):
		uploadFilesToGoogleDrive(globalUser)
		print("Wish to Continue ? ")
		inp = input("Hit 1 to Read OR 2 for New Record OR 3 to Upload: ")
		readJournalOrCreateJournal(inp, globalUser)
	elif(isRead == "E"):
		return
	else:
		inp = input("Wrong Input , Hit Again: ")
		readJournalOrCreateJournal(inp, globalUser)

def uploadFilesToGoogleDrive(globalUser):
	g_login = GoogleAuth()
	g_login.LocalWebserverAuth()
	drive = GoogleDrive(g_login)
	dirPath = globalUser + "_Notes"
	if(os.path.isdir(dirPath) == False):
		print("******   You Have Zero Journal   ******")
	else:
		file = open('key.key', 'rb')
		key = file.read()
		file.close()
		listOfFiles = os.listdir(dirPath)
		sortedListOfFiles = sorted(listOfFiles, key = int)
		count = 1
		print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		for fileX in sortedListOfFiles:
			print('\n' + "#Journal " + str(count) + '\n')
			filePath = dirPath + "/" + fileX
			ff = open(filePath, 'rb')
			fK = Fernet(key)
			ff_drive = drive.CreateFile({'title':os.path.basename('fn')})
			for line in ff:
				#print(fK.decrypt(line).decode())
				ff_drive.SetContentString(fK.decrypt(line).decode())
			#ff_drive.SetContentString(fK.decrypt(ff).decode().read())
			ff_drive.Upload()
			ff.close()
			print("***    Upload Complete   ***")

def readJornal(globalUser):
	dirPath = globalUser + "_Notes"
	if(os.path.isdir(dirPath) == False):
		print("******   You Have Zero Journal   ******")
	else:
		file = open('key.key', 'rb')
		key = file.read()
		file.close()
		listOfFiles = os.listdir(dirPath)
		sortedListOfFiles = sorted(listOfFiles, key = int)
		count = 1
		print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		for fileX in sortedListOfFiles:
			print('\n' + "#Journal " + str(count) + '\n')
			filePath = dirPath + "/" + fileX
			ff = open(filePath, 'rb')
			fK = Fernet(key)
			for line in ff:
				print(fK.decrypt(line).decode())
			print('\n' + '\n')
			count = count+1
			ff.close()
		print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")	
		
def newJournal(globalUser):
	dirPath = globalUser + "_Notes"
	today = date.today().strftime("%B %d, %Y")
	now = datetime.now().time().strftime("%H:%M:%S")
	userText = input("Hit :")
	if(userText != ""):
		
		if(os.path.isfile('key.key') == False):
			key = Fernet.generate_key()
			file = open('key.key', 'wb')
			file.write(key)
			file.close()
		
		file = open('key.key', 'rb')
		key = file.read()
		file.close()
		
		if(os.path.isdir(dirPath) == False):
			os.mkdir(dirPath)
		listOfFiles = os.listdir(dirPath)
		sortedListOfFiles = sorted(listOfFiles, key = int)
		index = -1
		if (len(listOfFiles) == 0):
			index = 1
		else:
			index = int(sortedListOfFiles[len(listOfFiles) - 1])+1
		if(len(listOfFiles) < 50):
			path = dirPath + "/" + str(index)
			f = open(path, 'wb')
			message = today + " " + now + '\n' + userText
			encrypted = message.encode()
			fK = Fernet(key)
			enc = fK.encrypt(encrypted)
			f.write(enc)
			f.close()
		else:
			delPath = dirPath + "/" + sortedListOfFiles[0]
			os.remove(delPath)
			path = dirPath + "/" + str(index)
			f = open(path, 'wb')
			message = today + " " + now + '\n' + userText
			encrypted = message.encode()
			fK = Fernet(key)
			enc = fK.encrypt(encrypted)
			f.write(enc)
			f.close()

def createUser(userName, password):
	if(os.path.isfile('usersList.txt')):
		f = open('usersList.txt', 'a')
		f.write('\n' + userName + " " + password)
		f.close()
		print("Created User")
	else:
		f = open('usersList.txt', 'a+')
		f.write(userName + " " + password)
		f.close()
		print("Created User")
	
def isDuplicateUser(userName):
	if(os.path.isfile('usersList.txt') == False):
		return 1
	f = open('usersList.txt', 'r')
	usersList = [l.strip().split()[0] for l in f]
	f.close()
	for user in usersList:
		if(user == userName):
			print("*****   User Already Exist With this username   *****")
			return 0;
	return 1;

def isValidCredentials(userName, password):
	if(os.path.isfile('usersList.txt') == False):
		print("*****    User Does Not Exist, Login Again   *****")
		return 0
	f = open('usersList.txt', 'r')
	usersList = [l.strip() for l in f]
	f.close()
	for userName_Password in usersList:
		name = userName_Password.split()[0];
		passw = userName_Password.split()[1];
		if(name == userName):
			if(password == passw):
				print("Welcome " + userName)
				return 1
			else:
				print("*****   Wrong Credentials, Login Again   *****")
				return 0
	print("*****  User Does Not Exist, Login Again   *****")
	return 0

def loginOrSignUp(isExist):
	if(isExist == "1"):
		userName = input("Username: ")
		password = getpass.getpass()
		while isValidCredentials(userName, password) == 0:
			wantToExit = input("HIT E For Exit OR Any Key To Continue: ")
			if(wantToExit == "E"):
				loginOrSignUp("E")
				return ["0"]
			else:
				userName = input("Username: ")
				password = getpass.getpass()
		globalUser = userName
		return ["1", globalUser]
	elif(isExist == "2"):
		print("Let's SignUp")
		userName = input("Username: ")
		password = getpass.getpass()
		while isDuplicateUser(userName) == 0:
			userName = input("Username: ")
			password = input("Password: ")
		createUser(userName, password)
		globalUser = userName
		return ["1", globalUser]
	elif(isExist == "E"):
		return ["0"]
	else:
		inp = input("Wrong Input, Hit Again: ")
		list = loginOrSignUp(inp)
		return list
		
# MAIN STARTS HERE		
print("Hit 1 for Login OR 2 for SignUp")
print("Hit E for Exit")

isExist = input("Hit: ")
if (isExist != "E"):
	toBeExited = loginOrSignUp(isExist)
	if(toBeExited[0] == "1"):
		print("Hit 1 for Read OR 2 for New Record OR 3 to Upload")
		print("Hit E for Exit")
		isRead = input("Hit: ")
		readJournalOrCreateJournal(isRead, toBeExited[1])
