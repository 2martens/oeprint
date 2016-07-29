# Printing Tool

This tool is used for the printing in the Orientation Unit of the
Computer Science department at the University of Hamburg.

It consists of two parts. The client part is a GUI application to select
the materials that should be printed. The server part is a CLI application
which will take commands and data from the client application.

## Requirements

The client application requires these things:

- Python 3.4
- PyQt 5 (GPL v3)
- Qt 5.3 (GPL v3)
- ssh

The server side requires this:

- Python 3.4
- PyPDF2 (bundled)
- lpr
- configured ssh server


## Getting started

The server part must be uploaded to the designated server location. The server must have Python 3.4 and lpr installed.
With this the server side is technically working. The next step is to update the data.json file which is filled
with the data for the Orientation Unit of the Computer Science department at the University of Hamburg. Your data
is likely different.

On the client side the contents of the client directory should be downloaded to a suitable place. The client
must have Python 3.4, PyQt 5, Qt 5.3 and ssh installed. The application is started by executing the main.py file.
The printer list in the config file most likely has to be changed as well for your demands. 


## FAQ

- Q: Upon the first start of program and subsequently whenever I want to print or synchronize the data, an OpenSSH dialog
appears and prompts for a passphrase. How can I prevent that?
A: That depends entirely on the ssh configuration on the server you are using. If the server requires password authentication,
there is nothing that can be done and you indeed have to enter the password every time.

- Q: The application looks boring. Why has it no graphics and beautiful vistas? 
A: Not necessary for functionality. You are invited to improve it though. 
