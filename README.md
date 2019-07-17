# Journal Application
A Command Line driven application which store personal journal log with user management

### Prerequisite 
Python 3.7.0 version of python and Command Line 

## Getting Started
Extract the ZIP (JOURNALAPP).
In windows you can start running the application by Opening JournalApp.exe.

If you are a Linux or MAC OS X User, Go to the src folder of the extracted zip and execute 

```
python JournalApp.py
```

We are now good to start with the application.


## Usage

In our application
```
Hit:   (This notifies that application is waiting for User Input)
````

While Running the application, you will be provided with two options Login/SignUp. 1 for Login OR 2 for SignUp
After succsesful authentication , you willbe provided with two entry to either read Previous Journals or create a new one.
User can exit out of application by pressing E keyword

```
Journals written by software cannot be read by any form of explorers.
I have used Fernet Encryption while writing Journal contents into file
```


## Files and Usage 

1. usersList -- This contains mapping between Username and Password (While Creating First User, This file will be created)
2. key.key -- Encryption and Decryption key to store message in encrypted format, This will be created first time and from next time it will be taken from the file.
3. src/JournalApp.py -- This is the source code written with python 3.7
4. **username_notes**
    will be a folder created for user to maintain it's notes.

**MANDATORY FILE** We only need JournalApp.exe file or the src to run our application, all the dependency file will be created or generated at the runtime as and when required.

### Build With
python 3.7.0

### Author
Mohammad Daud
mddaud4246@gmail.com
